from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

URL_DATABASE = "mysql+mysqlconnector://fastapi_user:supersecret@localhost/regis_db?charset=utf8mb4"

engine = create_engine(
    URL_DATABASE,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
