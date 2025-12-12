from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from app.core.config import settings
from typing import Optional


class MongoDBClient:
    """MongoDB client wrapper for master and tenant databases"""
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.master_db = None
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(
                settings.MONGODB_URL,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
            )
            # Verify connection
            self.client.admin.command("ping")
            self.master_db = self.client[settings.MASTER_DB_NAME]
            
            # Create indexes for master database
            self._create_master_db_indexes()
            print("✓ Connected to MongoDB")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"✗ Failed to connect to MongoDB: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            print("✓ Disconnected from MongoDB")
    
    def _create_master_db_indexes(self):
        """Create indexes for master database collections"""
        # Organizations collection
        organizations = self.master_db["organizations"]
        organizations.create_index("organization_name", unique=True)
        
        # Admin users collection
        admin_users = self.master_db["admin_users"]
        admin_users.create_index("email", unique=True)
        admin_users.create_index("organization_id")
    
    def get_master_db(self):
        """Get master database instance"""
        return self.master_db
    
    def get_tenant_db(self, org_name: str):
        """Get tenant database instance"""
        db_name = f"org_{org_name}"
        return self.client[db_name]
    
    def get_tenant_collection(self, org_name: str, collection_name: str = "data"):
        """Get tenant collection"""
        db = self.get_tenant_db(org_name)
        return db[collection_name]


# Global MongoDB client instance
mongodb_client = MongoDBClient()
