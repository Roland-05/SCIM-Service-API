from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class APIResponse(BaseModel):
    """
    Extend the API base schema for use as a GET request response schema.

    Reads data from SQLModel instances and serializes it into SCIM-compliant 
    JSON for FastAPI responses.
    """

    model_config = {
        "alias_generator": to_camel, # convert database ORM attributes to camel case to ensure SCIM compliant return (JSON).
        "populate_by_name": True, # populate the python attributes
        "from_attributes": True # read data from SQLModel instances
    }