
from sqlmodel import SQLmodel


class ImageCreate(SQLmodel):
    id: uuid.UUID
    url: str
