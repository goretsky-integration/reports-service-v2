from pydantic import BaseModel, conlist

from models.units import Unit

__all__ = ('Event',)


class Event(BaseModel):
    units: conlist(item_type=Unit, min_length=1)
    chat_ids: set[int]
