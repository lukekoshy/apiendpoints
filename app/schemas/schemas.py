from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class CreateOrganizationRequest(BaseModel):
    """Request schema for creating organization"""
    organization_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UpdateOrganizationRequest(BaseModel):
    """Request schema for updating organization"""
    organization_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)


class GetOrganizationRequest(BaseModel):
    """Request schema for getting organization"""
    organization_name: str = Field(..., min_length=1, max_length=100)


class DeleteOrganizationRequest(BaseModel):
    """Request schema for deleting organization"""
    organization_name: str = Field(..., min_length=1, max_length=100)


class AdminLoginRequest(BaseModel):
    """Request schema for admin login"""
    email: EmailStr
    password: str


class OrganizationResponse(BaseModel):
    """Response schema for organization"""
    organization_name: str
    collection_name: str
    admin_id: str
    created_at: datetime


class TokenResponse(BaseModel):
    """Response schema for token"""
    access_token: str
    token_type: str
    admin_id: str
    organization_id: str
    organization_name: str


class ErrorResponse(BaseModel):
    """Response schema for errors"""
    detail: str
    error_code: str


class SuccessResponse(BaseModel):
    """Generic success response"""
    message: str
    data: Optional[dict] = None
