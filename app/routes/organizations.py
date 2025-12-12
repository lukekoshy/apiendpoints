from fastapi import APIRouter, HTTPException, status, Depends, Header
from typing import Optional
from datetime import timedelta
from app.schemas.schemas import (
    CreateOrganizationRequest,
    UpdateOrganizationRequest,
    GetOrganizationRequest,
    DeleteOrganizationRequest,
    AdminLoginRequest,
    OrganizationResponse,
    TokenResponse,
    SuccessResponse,
)
from app.services.services import OrganizationService, AdminUserService
from app.core.security import create_access_token, decode_token
from app.core.config import settings

router = APIRouter(prefix="/org", tags=["organizations"])


@router.post("/create", response_model=dict)
async def create_organization(request: CreateOrganizationRequest):
    """Create a new organization"""
    success, org, message = OrganizationService.create_organization(
        organization_name=request.organization_name,
        email=request.email,
        password=request.password,
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )
    
    return {
        "message": "Organization created successfully",
        "data": {
            "organization_name": org.organization_name,
            "collection_name": org.collection_name,
            "admin_id": org.admin_id,
            "created_at": org.created_at.isoformat(),
        },
    }


@router.get("/get", response_model=dict)
async def get_organization(organization_name: str):
    """Get organization by name"""
    success, org, message = OrganizationService.get_organization(
        organization_name=organization_name
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )
    
    return {
        "message": "Organization retrieved successfully",
        "data": {
            "organization_name": org.organization_name,
            "collection_name": org.collection_name,
            "admin_id": org.admin_id,
            "created_at": org.created_at.isoformat(),
        },
    }


@router.put("/update", response_model=dict)
async def update_organization(
    request: UpdateOrganizationRequest,
    authorization: Optional[str] = Header(None),
):
    """Update organization (requires authentication)"""
    # Verify token
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
        )
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization",
        )
    
    success, org, message = OrganizationService.update_organization(
        organization_name=request.organization_name,
        email=request.email,
        password=request.password,
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )
    
    return {
        "message": "Organization updated successfully",
        "data": {
            "organization_name": org.organization_name,
            "collection_name": org.collection_name,
            "admin_id": org.admin_id,
        },
    }


@router.delete("/delete", response_model=dict)
async def delete_organization(
    organization_name: str,
    authorization: Optional[str] = Header(None),
):
    """Delete organization (requires authentication)"""
    # Verify token
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
        )
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization",
        )
    
    success, message = OrganizationService.delete_organization(
        organization_name=organization_name
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )
    
    return {"message": message}
