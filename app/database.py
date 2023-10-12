from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# username = "postgres"
# password = "Token@1234"
# host = "localhost"
# port = 5432
# db_name ="fastapi"

# SQLALCHEMY_DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/{db_name}'
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Token%401234@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine, autocommit=False)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()