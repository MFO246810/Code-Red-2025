import os
from models import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select, func

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()