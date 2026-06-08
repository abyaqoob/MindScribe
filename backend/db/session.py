from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from core.config import settings

db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)
elif db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(db_url, pool_pre_ping=True) # why 2nd parameter ?

@event.listens_for(engine, "connect")
def provide_vector_extension(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector") # toggling vecotr extension
    cursor.close()

SessionLocal = sessionmaker(bind=engine) # getting session to db 

# Dependency to get DB session in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()