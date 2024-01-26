from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api import user, users, auth, like, static

app = FastAPI(
    redoc_url='/api/docs'
)

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Including API routers
app.include_router(user.router, prefix="/user")
app.include_router(users.router, prefix="/users")
app.include_router(auth.router, prefix="/auth")
app.include_router(like.router, prefix="/like")
app.include_router(static.router, prefix="/static")
# app.include_router(settings.router, prefix="/settings", tags=["settings"])
