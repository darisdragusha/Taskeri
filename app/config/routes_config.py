
# Define public routes that don't require authentication
PUBLIC_ROUTES = [
    "/login", 
    "/register", 
    "/docs", 
    "/openapi.json", 
    "/token", 
    "/tenant-users",
    "/tenant-users/"
]

# Define route permissions mapping - regexes are used for pattern matching
ROUTE_PERMISSIONS = {
    # Company routes
    r"^/companies/?$": {
        "GET": ["read_company"],
        "POST": ["create_company"]
    },
    r"^/companies/\d+$": {
        "GET": ["read_company"],
        "PUT": ["update_company"],
        "DELETE": ["delete_company"]
    },
    
    # Role routes
    r"^/roles$": {
        "GET": ["read_role"],
        "POST": ["create_role"]
    },
    r"^/roles/\d+$": {
        "GET": ["read_role"],
    }
}
