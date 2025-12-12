import re


def sanitize_org_name(org_name: str) -> str:
    """Sanitize organization name for use in database/collection names"""
    # Convert to lowercase, replace spaces and special chars with underscores
    sanitized = re.sub(r"[^a-z0-9_]", "_", org_name.lower())
    # Remove leading/trailing underscores
    sanitized = sanitized.strip("_")
    # Replace multiple underscores with single
    sanitized = re.sub(r"_+", "_", sanitized)
    return sanitized


def validate_org_name(org_name: str) -> bool:
    """Validate organization name format"""
    # Allow alphanumeric, spaces, hyphens, underscores
    pattern = r"^[a-zA-Z0-9\s\-_]{1,100}$"
    return bool(re.match(pattern, org_name))
