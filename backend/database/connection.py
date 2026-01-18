"""
Database Connection Module
Handles connection to PostgreSQL/Supabase (future implementation)
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)

# Database URL from environment variable
# Format: postgresql://user:password@host:port/database
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_database_engine():
    """
    Create and return a database engine.

    Returns:
        SQLAlchemy engine instance
    """
    if not DATABASE_URL:
        logger.warning("DATABASE_URL not set, database features disabled")
        return None

    try:
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,  # Verify connections before using
            pool_size=5,  # Connection pool size
            max_overflow=10  # Max connections beyond pool_size
        )
        logger.info("Database engine created successfully")
        return engine
    except Exception as e:
        logger.error(f"Failed to create database engine: {str(e)}", exc_info=True)
        raise

def get_session_maker():
    """
    Create and return a session maker.

    Returns:
        SQLAlchemy sessionmaker
    """
    engine = get_database_engine()
    if not engine:
        return None

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

def get_db():
    """
    Dependency for FastAPI routes to get database session.

    Usage:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()

    Yields:
        Database session
    """
    SessionLocal = get_session_maker()
    if not SessionLocal:
        raise Exception("Database not configured")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """
    Initialize database tables.
    Creates all tables defined in models.py
    """
    from database.models import Base

    engine = get_database_engine()
    if not engine:
        logger.warning("Skipping database initialization (no DATABASE_URL)")
        return

    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}", exc_info=True)
        raise

# TODO: Add when ready to use database
# Uncomment in backend/main.py startup event:
# @app.on_event("startup")
# async def startup():
#     init_database()
