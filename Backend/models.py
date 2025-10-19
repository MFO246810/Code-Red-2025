import enum
import datetime
from typing import List
from sqlalchemy import (Column, BigInteger, String, Text, TIMESTAMP, ForeignKey, JSON)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "User"

    User_ID = Column(BigInteger, primary_key=True, nullable=False)
    Email = Column(String(255), nullable=False)
    Password = Column(String(255), nullable=False)
    UserName = Column(String(255), nullable=False)
    Created_at = Column(TIMESTAMP, nullable=False)

    # Relationships
    photos = relationship("User_Photo", back_populates="user")
    logs = relationship("Logs", back_populates="user")


class User_Photo(Base):
    __tablename__ = "User_Photo"

    Photo_ID = Column(BigInteger, primary_key=True, nullable=False)
    User_ID = Column(BigInteger, ForeignKey("User.User_ID"), nullable=False)
    Image_Url = Column(Text, nullable=False)
    Caption = Column(Text, nullable=False)
    Created_At = Column(TIMESTAMP, nullable=False)
    Location = Column(Text, nullable=False)

    # Relationships
    user = relationship("User", back_populates="photos")
    logs = relationship("Logs", back_populates="user_photo")


class Output_Photo(Base):
    __tablename__ = "Output_Photo"

    Photo_ID = Column(BigInteger, primary_key=True, nullable=False)
    Image_Url = Column(Text, nullable=False)
    Caption = Column(Text, nullable=False)
    Created_At = Column(TIMESTAMP, nullable=False)

    # Relationships
    logs = relationship("Logs", back_populates="output_photo")


class Logs(Base):
    __tablename__ = "Logs"

    Log_ID = Column(BigInteger, primary_key=True, nullable=False)
    User_ID = Column(BigInteger, ForeignKey("User.User_ID"), nullable=False)
    User_Photo_ID = Column(BigInteger, ForeignKey("User_Photo.Photo_ID"), nullable=False)
    Output_Photo_ID = Column(BigInteger, ForeignKey("Output_Photo.Photo_ID"), nullable=False)
    Tags = Column(String(255), nullable=False)
    Created_at = Column(TIMESTAMP, nullable=False)
    Calibration = Column(JSON, nullable=False)
    Description = Column(Text, nullable=False)

    # Relationships
    user = relationship("User", back_populates="logs")
    user_photo = relationship("User_Photo", back_populates="logs")
    output_photo = relationship("Output_Photo", back_populates="logs")
