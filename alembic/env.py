from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.database import Base  

# config object
config = context.config

# env var ကနေ Database URL ယူ
import os
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Base metadata assign
target_metadata = Base.metadata
