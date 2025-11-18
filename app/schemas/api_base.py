from pydantic import BaseModel

def to_snake(string: str) -> str:
    out = []

    for char in string:
        if char.isupper():
            out.append('_')
            out.append(char.lower())

        else:
            out.append(char)

    return ''.join(out)

# Define a base Schema class using alias_generator
