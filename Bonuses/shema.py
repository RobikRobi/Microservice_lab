from pydantic import BaseModel



class BonusUpdate(BaseModel):
    bonuses: int