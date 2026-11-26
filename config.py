import os
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-before-deploy")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///merlin.db").replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
