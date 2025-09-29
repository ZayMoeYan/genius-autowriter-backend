# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Use NullPool when connecting through pgbouncer transaction mode
from sqlalchemy.pool import NullPool

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

# If you use Supabase pooler in transaction mode, prefer NullPool (avoid double pooling).
# If you have a long-running VM / container, you can configure a QueuePool instead.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    poolclass=NullPool,   # recommended with PgBouncer transaction mode / serverless
    future=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
