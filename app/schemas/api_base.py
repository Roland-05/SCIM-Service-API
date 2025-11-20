from pydantic import BaseModel
from pydantic.alias_generators import to_camel

# Define a base Schema class using alias_generator

class APIBase(BaseModel):
    model_config = {
        "alias_generator": to_camel, # applied during serialisation
        "populate_by_name": True, # Assign values using snake_case attribute names.
    } 
