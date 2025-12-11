# PowerShell curl examples for testing the Multi-Tenant API
# Save as: curl_examples.ps1
# Run with: .\curl_examples.ps1

# Configuration
$API_URL = "http://localhost:8000"
$ORG_NAME = "Test Organization"
$ADMIN_EMAIL = "admin@testorg.com"
$ADMIN_PASSWORD = "TestPassword123!"

Write-Host "Multi-Tenant API - PowerShell curl Examples" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Health Check
Write-Host "1. Health Check" -ForegroundColor Green
Write-Host "Command:"
Write-Host "curl.exe $API_URL/health"
Write-Host ""
Write-Host "Response:"
curl.exe -s "$API_URL/health" | ConvertFrom-Json | ConvertTo-Json
Write-Host ""
Write-Host ""

# Create Organization
Write-Host "2. Create Organization" -ForegroundColor Green
Write-Host "Command:"
Write-Host "curl.exe -X POST $API_URL/org/create -H 'Content-Type: application/json' -d '{...}'"
Write-Host ""
Write-Host "Response:"
$response = curl.exe -s -X POST "$API_URL/org/create" `
  -H "Content-Type: application/json" `
  -d @"
{
  "organization_name": "$ORG_NAME",
  "email": "$ADMIN_EMAIL",
  "password": "$ADMIN_PASSWORD"
}
"@
$response | ConvertFrom-Json | ConvertTo-Json
Write-Host ""
Write-Host ""

# Get Organization
Write-Host "3. Get Organization" -ForegroundColor Green
Write-Host "Command:"
Write-Host "curl.exe -s '$API_URL/org/get?organization_name=$ORG_NAME'"
Write-Host ""
Write-Host "Response:"
curl.exe -s "$API_URL/org/get?organization_name=$ORG_NAME" | ConvertFrom-Json | ConvertTo-Json
Write-Host ""
Write-Host ""

# Admin Login
Write-Host "4. Admin Login" -ForegroundColor Green
Write-Host "Command:"
Write-Host "curl.exe -X POST $API_URL/admin/login -H 'Content-Type: application/json' -d '{...}'"
Write-Host ""
Write-Host "Response:"
$loginResponse = curl.exe -s -X POST "$API_URL/admin/login" `
  -H "Content-Type: application/json" `
  -d @"
{
  "email": "$ADMIN_EMAIL",
  "password": "$ADMIN_PASSWORD"
}
"@
$loginResponse | ConvertFrom-Json | ConvertTo-Json
Write-Host ""

# Extract token from login response
try {
  $loginData = $loginResponse | ConvertFrom-Json
  $token = $loginData.data.access_token
  
  if ($token) {
    Write-Host "✓ Token extracted: $($token.Substring(0, 50))..."
    Write-Host ""
    Write-Host ""

    # Update Organization
    Write-Host "5. Update Organization (requires token)" -ForegroundColor Green
    Write-Host "Command:"
    Write-Host "curl.exe -X PUT $API_URL/org/update -H 'Authorization: Bearer <token>' -d '{...}'"
    Write-Host ""
    Write-Host "Response:"
    curl.exe -s -X PUT "$API_URL/org/update" `
      -H "Content-Type: application/json" `
      -H "Authorization: Bearer $token" `
      -d @"
{
  "organization_name": "$ORG_NAME",
  "email": "new@testorg.com",
  "password": "NewPassword123!"
}
"@ | ConvertFrom-Json | ConvertTo-Json
    Write-Host ""
    Write-Host ""

    # Delete Organization
    Write-Host "6. Delete Organization (requires token)" -ForegroundColor Green
    Write-Host "Command:"
    Write-Host "curl.exe -X DELETE '$API_URL/org/delete?organization_name=$ORG_NAME' -H 'Authorization: Bearer <token>'"
    Write-Host ""
    Write-Host "Response:"
    curl.exe -s -X DELETE "$API_URL/org/delete?organization_name=$ORG_NAME" `
      -H "Authorization: Bearer $token" | ConvertFrom-Json | ConvertTo-Json
    Write-Host ""
  }
  else {
    Write-Host "✗ Failed to extract token from login response" -ForegroundColor Red
    Write-Host ""
  }
}
catch {
  Write-Host "✗ Error processing login response: $_" -ForegroundColor Red
  Write-Host ""
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "curl Examples Complete!" -ForegroundColor Cyan
