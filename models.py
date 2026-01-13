from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    brand = Column(String)
    category = Column(String)
    retailer = Column(String)
    url = Column(String, unique=True)
    image_url = Column(String, nullable=True)
    tags = Column(String)

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    # CHANGED: Added ForeignKey to enforce valid product IDs
    product_id = Column(Integer, ForeignKey("products.id")) 
    event_type = Column(String)  # e.g., "view_product", "click_out"
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # CHANGED: Added relationship for easy access to Product data from an Event
    product = relationship("Product")