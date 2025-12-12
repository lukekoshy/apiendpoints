from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from app.schemas.schemas import AdminLoginRequest, TokenResponse
from app.services.services import AdminUserService
from app.core.security import create_access_token

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/login", response_model=dict)
async def admin_login(request: AdminLoginRequest):
    """Admin login endpoint"""
    success, admin_user, message = AdminUserService.authenticate(
        email=request.email,
        password=request.password,
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )
    
    # Get organization details
    org_success, org, org_message = AdminUserService.get_organization_by_admin(
        admin_id=str(admin_user._id)
    )
    
    if not org_success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=org_message,
        )
    
    # Create access token
    token_data = {
        "sub": str(admin_user._id),
        "admin_id": str(admin_user._id),
        "organization_id": str(org._id),
        "organization_name": org.organization_name,
        "email": admin_user.email,
    }
    access_token = create_access_token(data=token_data)
    
    return {
        "message": "Login successful",
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "admin_id": str(admin_user._id),
            "organization_id": str(org._id),
            "organization_name": org.organization_name,
        },
    }
