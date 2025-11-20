from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class APIResponse(BaseModel):
    model_config = {
        "alias_generator": to_camel, # during serialisation
        "populate_by_name": True, # populate the python attributes
        "from_attributes": True # read data from SQLModel instances
    }