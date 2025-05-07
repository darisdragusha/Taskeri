from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from views import routers
from middleware import MultiTenantMiddleware  

app = FastAPI()

# CORS Configuration
allowed_origins = ["http://localhost", "http://127.0.0.1:8000", '*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add MultiTenantMiddleware to the FastAPI app
app.add_middleware(MultiTenantMiddleware)

# Include routers
for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    import os
    import uvicorn

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("app:app", host=host, port=port, reload=True)
