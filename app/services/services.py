from typing import Optional, Tuple
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from app.db.mongodb import mongodb_client
from app.models.models import Organization, AdminUser
from app.core.password import hash_password, verify_password
from app.utils.validators import sanitize_org_name, validate_org_name


class OrganizationService:
    """Service for organization operations"""
    
    @staticmethod
    def create_organization(
        organization_name: str, email: str, password: str
    ) -> Tuple[bool, Optional[Organization], str]:
        """
        Create a new organization with admin user
        
        Returns:
            Tuple[success: bool, organization: Organization, message: str]
        """
        try:
            # Validate organization name
            if not validate_org_name(organization_name):
                return False, None, "Invalid organization name format"
            
            master_db = mongodb_client.get_master_db()
            orgs_collection = master_db["organizations"]
            
            # Check if organization already exists
            existing_org = orgs_collection.find_one(
                {"organization_name": organization_name}
            )
            if existing_org:
                return False, None, "Organization already exists"
            
            # Create admin user
            hashed_password = hash_password(password)
            admin_user = AdminUser(
                email=email,
                hashed_password=hashed_password,
                organization_id=str(ObjectId()),  # Temporary, will update after org creation
            )
            
            # Create organization
            collection_name = f"org_{sanitize_org_name(organization_name)}"
            org = Organization(
                organization_name=organization_name,
                collection_name=collection_name,
                admin_id=str(admin_user._id),
            )
            
            # Insert organization
            org_result = orgs_collection.insert_one(org.to_dict())
            org_id = str(org_result.inserted_id)
            
            # Update admin user with organization ID and insert
            admin_user.organization_id = org_id
            admin_users_collection = master_db["admin_users"]
            admin_users_collection.insert_one(admin_user.to_dict())
            
            # Create tenant database collection (creates database if not exists)
            tenant_db = mongodb_client.get_tenant_db(organization_name)
            tenant_db.create_collection("data")
            
            # Retrieve the created organization
            org_data = orgs_collection.find_one({"_id": ObjectId(org_id)})
            created_org = Organization.from_dict(org_data)
            
            return True, created_org, "Organization created successfully"
            
        except DuplicateKeyError:
            return False, None, "Email already registered"
        except Exception as e:
            return False, None, f"Error creating organization: {str(e)}"
    
    @staticmethod
    def get_organization(organization_name: str) -> Tuple[bool, Optional[Organization], str]:
        """
        Get organization by name
        
        Returns:
            Tuple[success: bool, organization: Organization, message: str]
        """
        try:
            master_db = mongodb_client.get_master_db()
            orgs_collection = master_db["organizations"]
            
            org_data = orgs_collection.find_one(
                {"organization_name": organization_name}
            )
            
            if not org_data:
                return False, None, "Organization not found"
            
            org = Organization.from_dict(org_data)
            return True, org, "Organization retrieved successfully"
            
        except Exception as e:
            return False, None, f"Error retrieving organization: {str(e)}"
    
    @staticmethod
    def update_organization(
        organization_name: str, email: str, password: str
    ) -> Tuple[bool, Optional[Organization], str]:
        """
        Update organization (change admin credentials and collection)
        
        Returns:
            Tuple[success: bool, organization: Organization, message: str]
        """
        try:
            master_db = mongodb_client.get_master_db()
            orgs_collection = master_db["organizations"]
            admin_users_collection = master_db["admin_users"]
            
            # Get existing organization
            org_data = orgs_collection.find_one(
                {"organization_name": organization_name}
            )
            
            if not org_data:
                return False, None, "Organization not found"
            
            org_id = str(org_data["_id"])
            old_collection_name = org_data["collection_name"]
            
            # Create new collection name
            new_collection_name = f"org_{sanitize_org_name(organization_name)}_v2"
            
            # Migrate data from old collection to new collection
            try:
                old_db = mongodb_client.get_tenant_db(organization_name)
                old_collection = old_db[old_collection_name.replace("org_", "").replace(f"_{sanitize_org_name(organization_name)}", "")]
                
                new_db = mongodb_client.get_tenant_db(organization_name)
                new_collection = new_db["data_v2"]
                
                # Copy all documents
                if old_collection.count_documents({}) > 0:
                    documents = list(old_collection.find({}))
                    if documents:
                        new_collection.insert_many(documents)
            except Exception as migration_error:
                # If migration fails, still allow update but log the error
                print(f"Warning: Data migration failed: {migration_error}")
            
            # Update organization with new collection name
            orgs_collection.update_one(
                {"_id": ObjectId(org_id)},
                {
                    "$set": {
                        "collection_name": new_collection_name,
                    }
                },
            )
            
            # Update admin password
            hashed_password = hash_password(password)
            admin_users_collection.update_one(
                {"organization_id": org_id, "email": email},
                {"$set": {"hashed_password": hashed_password}},
            )
            
            # Retrieve updated organization
            updated_org_data = orgs_collection.find_one({"_id": ObjectId(org_id)})
            updated_org = Organization.from_dict(updated_org_data)
            
            return True, updated_org, "Organization updated successfully"
            
        except Exception as e:
            return False, None, f"Error updating organization: {str(e)}"
    
    @staticmethod
    def delete_organization(organization_name: str) -> Tuple[bool, str]:
        """
        Delete organization and its collections
        
        Returns:
            Tuple[success: bool, message: str]
        """
        try:
            master_db = mongodb_client.get_master_db()
            orgs_collection = master_db["organizations"]
            admin_users_collection = master_db["admin_users"]
            
            # Get organization
            org_data = orgs_collection.find_one(
                {"organization_name": organization_name}
            )
            
            if not org_data:
                return False, "Organization not found"
            
            org_id = str(org_data["_id"])
            
            # Delete admin users
            admin_users_collection.delete_many({"organization_id": org_id})
            
            # Delete organization
            orgs_collection.delete_one({"_id": ObjectId(org_id)})
            
            # Drop tenant database
            try:
                tenant_db = mongodb_client.get_tenant_db(organization_name)
                mongodb_client.client.drop_database(tenant_db.name)
            except Exception as db_error:
                print(f"Warning: Failed to drop database: {db_error}")
            
            return True, "Organization deleted successfully"
            
        except Exception as e:
            return False, f"Error deleting organization: {str(e)}"


class AdminUserService:
    """Service for admin user operations"""
    
    @staticmethod
    def authenticate(email: str, password: str) -> Tuple[bool, Optional[AdminUser], str]:
        """
        Authenticate admin user
        
        Returns:
            Tuple[success: bool, admin_user: AdminUser, message: str]
        """
        try:
            master_db = mongodb_client.get_master_db()
            admin_users_collection = master_db["admin_users"]
            
            admin_data = admin_users_collection.find_one({"email": email})
            
            if not admin_data:
                return False, None, "Invalid email or password"
            
            admin_user = AdminUser.from_dict(admin_data)
            
            # Verify password
            if not verify_password(password, admin_user.hashed_password):
                return False, None, "Invalid email or password"
            
            return True, admin_user, "Authentication successful"
            
        except Exception as e:
            return False, None, f"Error authenticating user: {str(e)}"
    
    @staticmethod
    def get_admin_by_id(admin_id: str) -> Tuple[bool, Optional[AdminUser], str]:
        """Get admin user by ID"""
        try:
            master_db = mongodb_client.get_master_db()
            admin_users_collection = master_db["admin_users"]
            
            admin_data = admin_users_collection.find_one({"_id": ObjectId(admin_id)})
            
            if not admin_data:
                return False, None, "Admin user not found"
            
            admin_user = AdminUser.from_dict(admin_data)
            return True, admin_user, "Admin retrieved successfully"
            
        except Exception as e:
            return False, None, f"Error retrieving admin: {str(e)}"
    
    @staticmethod
    def get_organization_by_admin(admin_id: str) -> Tuple[bool, Optional[Organization], str]:
        """Get organization by admin ID"""
        try:
            master_db = mongodb_client.get_master_db()
            admin_users_collection = master_db["admin_users"]
            orgs_collection = master_db["organizations"]
            
            admin_data = admin_users_collection.find_one({"_id": ObjectId(admin_id)})
            
            if not admin_data:
                return False, None, "Admin not found"
            
            org_data = orgs_collection.find_one(
                {"_id": ObjectId(admin_data["organization_id"])}
            )
            
            if not org_data:
                return False, None, "Organization not found"
            
            org = Organization.from_dict(org_data)
            return True, org, "Organization retrieved"
            
        except Exception as e:
            return False, None, f"Error retrieving organization: {str(e)}"
