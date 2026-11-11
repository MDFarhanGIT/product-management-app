from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# db_url = "postgresql://postgres:Farhan@3935@localhost:5432/Farhan_db"
# db_url = "postgresql+psycopg2://postgres:Farhan@3935@localhost:5432/Farhan_db"
db_url = "postgresql://postgres:Farhan%403935@localhost:5432/Farhan_db"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

