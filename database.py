from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

pymysql.install_as_MySQLdb()

# Format: mysql+pymysql://username:password@host:port/dbname
DATABASE_URL= "mysql+pymysql://root@localhost:3306/fastapi_db"
# DATABASE_URL = "mysql://root:ZBPvgDoiAOCgjhDZFLfwzMRaafAMKAko@trolley.proxy.rlwy.net:11430/railway"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()