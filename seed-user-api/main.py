from fastapi import FastAPI, Depends
from auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from auth import verify_token
app = FastAPI()
app.include_router(auth_router, prefix="/auth")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "FastAPI Auth with RBAC"}


@app.get("/protected")
async def protected_route(user: str = Depends(verify_token)):
    return {"message": f"Hello, {user}! You have access to this route."}
