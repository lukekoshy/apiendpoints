from datetime import datetime
from typing import Optional
from bson import ObjectId


class Organization:
    """Organization model for master database"""
    
    def __init__(
        self,
        organization_name: str,
        collection_name: str,
        admin_id: str,
        created_at: Optional[datetime] = None,
        _id: Optional[ObjectId] = None,
    ):
        self._id = _id or ObjectId()
        self.organization_name = organization_name
        self.collection_name = collection_name
        self.admin_id = admin_id
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "_id": self._id,
            "organization_name": self.organization_name,
            "collection_name": self.collection_name,
            "admin_id": self.admin_id,
            "created_at": self.created_at,
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Organization":
        """Create from dictionary"""
        return Organization(
            organization_name=data.get("organization_name"),
            collection_name=data.get("collection_name"),
            admin_id=data.get("admin_id"),
            created_at=data.get("created_at"),
            _id=data.get("_id"),
        )


class AdminUser:
    """Admin user model for master database"""
    
    def __init__(
        self,
        email: str,
        hashed_password: str,
        organization_id: str,
        created_at: Optional[datetime] = None,
        _id: Optional[ObjectId] = None,
    ):
        self._id = _id or ObjectId()
        self.email = email
        self.hashed_password = hashed_password
        self.organization_id = organization_id
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "_id": self._id,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "organization_id": self.organization_id,
            "created_at": self.created_at,
        }
    
    @staticmethod
    def from_dict(data: dict) -> "AdminUser":
        """Create from dictionary"""
        return AdminUser(
            email=data.get("email"),
            hashed_password=data.get("hashed_password"),
            organization_id=data.get("organization_id"),
            created_at=data.get("created_at"),
            _id=data.get("_id"),
        )
