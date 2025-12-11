"""
Example test script demonstrating API usage.

Run the FastAPI application first:
    uvicorn app.main:app --reload

Then run this script:
    python test_api.py
"""

import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000"


class APIClient:
    """Simple API client for testing"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.token: Optional[str] = None
    
    def health_check(self):
        """Check API health"""
        print("\n📋 Health Check")
        print("-" * 50)
        response = requests.get(f"{self.base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json()
    
    def create_organization(self, org_name: str, email: str, password: str):
        """Create new organization"""
        print(f"\n🏢 Creating Organization: {org_name}")
        print("-" * 50)
        
        payload = {
            "organization_name": org_name,
            "email": email,
            "password": password,
        }
        
        response = requests.post(
            f"{self.base_url}/org/create",
            json=payload,
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json()
    
    def get_organization(self, org_name: str):
        """Get organization details"""
        print(f"\n🔍 Getting Organization: {org_name}")
        print("-" * 50)
        
        response = requests.get(
            f"{self.base_url}/org/get",
            params={"organization_name": org_name},
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json()
    
    def admin_login(self, email: str, password: str):
        """Admin login"""
        print(f"\n🔐 Admin Login: {email}")
        print("-" * 50)
        
        payload = {
            "email": email,
            "password": password,
        }
        
        response = requests.post(
            f"{self.base_url}/admin/login",
            json=payload,
        )
        
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 200 and "data" in result:
            self.token = result["data"]["access_token"]
            print(f"✓ Token saved for future requests")
        
        return result
    
    def update_organization(self, org_name: str, email: str, password: str):
        """Update organization"""
        print(f"\n✏️  Updating Organization: {org_name}")
        print("-" * 50)
        
        if not self.token:
            print("❌ No token available. Please login first.")
            return None
        
        payload = {
            "organization_name": org_name,
            "email": email,
            "password": password,
        }
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.put(
            f"{self.base_url}/org/update",
            json=payload,
            headers=headers,
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json()
    
    def delete_organization(self, org_name: str):
        """Delete organization"""
        print(f"\n🗑️  Deleting Organization: {org_name}")
        print("-" * 50)
        
        if not self.token:
            print("❌ No token available. Please login first.")
            return None
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.delete(
            f"{self.base_url}/org/delete",
            params={"organization_name": org_name},
            headers=headers,
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json()


def main():
    """Run example tests"""
    
    print("=" * 50)
    print("Multi-Tenant API Test Script")
    print("=" * 50)
    
    client = APIClient()
    
    # 1. Health Check
    client.health_check()
    
    # 2. Create Organization
    org_name = "Test Organization"
    email = "admin@testorg.com"
    password = "TestPassword123!"
    
    create_result = client.create_organization(org_name, email, password)
    
    if create_result.get("message") == "Organization created successfully":
        print("✓ Organization created successfully")
        
        # 3. Get Organization
        client.get_organization(org_name)
        
        # 4. Admin Login
        login_result = client.admin_login(email, password)
        
        if login_result.get("message") == "Login successful":
            print("✓ Login successful")
            
            # 5. Update Organization
            new_email = "newemail@testorg.com"
            new_password = "NewPassword123!"
            client.update_organization(org_name, new_email, new_password)
            
            # 6. Login with new credentials
            print("\n🔐 Login with New Credentials")
            print("-" * 50)
            client.admin_login(new_email, new_password)
            
            # 7. Delete Organization
            client.delete_organization(org_name)
        else:
            print("❌ Login failed")
    else:
        print(f"❌ Failed to create organization: {create_result}")
    
    print("\n" + "=" * 50)
    print("Test Complete!")
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API!")
        print("Make sure the FastAPI server is running:")
        print("  uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
