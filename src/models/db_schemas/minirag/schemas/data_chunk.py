from .minirag_base import SQLAlchemyBase

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import Index
import uuid




class DataChunk(SQLAlchemyBase):
    
    __tablename__ = "chunks"