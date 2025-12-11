#!/usr/bin/env bash
# curl_examples.sh
# Example curl commands for testing the Multi-Tenant API

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
API_URL="http://localhost:8000"
ORG_NAME="Test Organization"
ADMIN_EMAIL="admin@testorg.com"
ADMIN_PASSWORD="TestPassword123!"

echo -e "${BLUE}Multi-Tenant API - curl Examples${NC}"
echo "=================================="
echo ""

# Health Check
echo -e "${GREEN}1. Health Check${NC}"
echo "Command:"
echo "curl $API_URL/health"
echo ""
echo "Response:"
curl -s $API_URL/health | python -m json.tool
echo ""
echo ""

# Create Organization
echo -e "${GREEN}2. Create Organization${NC}"
echo "Command:"
echo "curl -X POST $API_URL/org/create \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"organization_name\": \"$ORG_NAME\", \"email\": \"$ADMIN_EMAIL\", \"password\": \"$ADMIN_PASSWORD\"}'"
echo ""
echo "Response:"
RESPONSE=$(curl -s -X POST $API_URL/org/create \
  -H "Content-Type: application/json" \
  -d "{
    \"organization_name\": \"$ORG_NAME\",
    \"email\": \"$ADMIN_EMAIL\",
    \"password\": \"$ADMIN_PASSWORD\"
  }")
echo "$RESPONSE" | python -m json.tool
echo ""
echo ""

# Get Organization
echo -e "${GREEN}3. Get Organization${NC}"
echo "Command:"
echo "curl '$API_URL/org/get?organization_name=$ORG_NAME'"
echo ""
echo "Response:"
curl -s "$API_URL/org/get?organization_name=$ORG_NAME" | python -m json.tool
echo ""
echo ""

# Admin Login
echo -e "${GREEN}4. Admin Login${NC}"
echo "Command:"
echo "curl -X POST $API_URL/admin/login \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"email\": \"$ADMIN_EMAIL\", \"password\": \"$ADMIN_PASSWORD\"}'"
echo ""
echo "Response:"
LOGIN_RESPONSE=$(curl -s -X POST $API_URL/admin/login \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$ADMIN_EMAIL\",
    \"password\": \"$ADMIN_PASSWORD\"
  }")
echo "$LOGIN_RESPONSE" | python -m json.tool
echo ""

# Extract token from login response
TOKEN=$(echo "$LOGIN_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])" 2>/dev/null)

if [ ! -z "$TOKEN" ]; then
  echo "✓ Token extracted: ${TOKEN:0:50}..."
  echo ""
  echo ""

  # Update Organization
  echo -e "${GREEN}5. Update Organization (requires token)${NC}"
  echo "Command:"
  echo "curl -X PUT $API_URL/org/update \\"
  echo "  -H 'Content-Type: application/json' \\"
  echo "  -H 'Authorization: Bearer <token>' \\"
  echo "  -d '{\"organization_name\": \"$ORG_NAME\", \"email\": \"new@testorg.com\", \"password\": \"NewPassword123!\"}'"
  echo ""
  echo "Response:"
  curl -s -X PUT $API_URL/org/update \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d "{
      \"organization_name\": \"$ORG_NAME\",
      \"email\": \"new@testorg.com\",
      \"password\": \"NewPassword123!\"
    }" | python -m json.tool
  echo ""
  echo ""

  # Delete Organization
  echo -e "${GREEN}6. Delete Organization (requires token)${NC}"
  echo "Command:"
  echo "curl -X DELETE '$API_URL/org/delete?organization_name=$ORG_NAME' \\"
  echo "  -H 'Authorization: Bearer <token>'"
  echo ""
  echo "Response:"
  curl -s -X DELETE "$API_URL/org/delete?organization_name=$ORG_NAME" \
    -H "Authorization: Bearer $TOKEN" | python -m json.tool
  echo ""
else
  echo -e "${RED}✗ Failed to extract token from login response${NC}"
  echo ""
fi

echo -e "${BLUE}=================================="
echo "curl Examples Complete!${NC}"
