
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class RecommendationItem(BaseModel):
    id: int
    title: str
    price: float
    score: int
    reason: str
    image_url: str | None
    url: str | None

# IMPROVEMENT: Enforce valid event types using an Enum
class EventType(str, Enum):
    VIEW = "view_product"
    CLICK = "click_out"
    SAVE = "save_product"

class RecommendationRequest(BaseModel):
    recipient_age: int
    occasion: str
    relationship: str
    budget: float
    interests: List[str]

class EventRequest(BaseModel):
    user_id: str
    product_id: int
    event_type: EventType  # IMPROVEMENT: Uses Enum validation