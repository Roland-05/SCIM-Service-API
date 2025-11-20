from pydantic import BaseModel
def to_camel(string: str) -> str:
    
    parts = string.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

class APIResponse(BaseModel):
    model_config = {
        "alias_generator": to_camel, # during serialisation
        "populate_by_name": True, 
        "from_attributes": True # read data from SQLModel instances
    }