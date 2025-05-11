from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Charge(BaseModel):
    user_id: str
    amount: float
    currency: str
    timestamp: datetime

class Alert(BaseModel):
    user_id: str
    reason: str
    charge: Optional[Charge] = None
    related_charges: Optional[List[Charge]] = None 