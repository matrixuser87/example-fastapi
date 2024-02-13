from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models, config
from .database import engine
from .routers import post, user, auth, vote

print(config.settings.database_password)

# Create tables from the models instead of using alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)