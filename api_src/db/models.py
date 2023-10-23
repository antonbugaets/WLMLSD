import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    registration_date = Column(DateTime, default=datetime.utcnow)

    name = Column(String, nullable=False)

    total_created = Column(Integer, nullable=False, default=0)
