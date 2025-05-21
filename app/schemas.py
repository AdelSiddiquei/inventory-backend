from pydantic import BaseModel, ConfigDict


class inventory(BaseModel):
    item: str
    description: str = 'Not Provided'
    price: float

    model_config = 