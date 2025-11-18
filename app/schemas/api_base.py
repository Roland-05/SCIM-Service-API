from pydantic import BaseModel
from pydantic.alias_generators import to_snake

# Define a base Schema class using alias_generator

class APIBase(BaseModel):
    model_config = {
        "alias_generator": to_snake, # applied during serialisation
        "populate_by_name": True, # Assign values using snake_case attribute names.
    }