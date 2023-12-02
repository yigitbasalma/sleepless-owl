from sqlalchemy import create_engine

from w.config.config import SQLALCHEMY_ENGINE_OPTIONS, SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, **SQLALCHEMY_ENGINE_OPTIONS)
