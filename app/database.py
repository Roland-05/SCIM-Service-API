from sqlmodel import Field, SQLModel, Session, create_engine



# create the DB engine

engine = create_engine("sqlite:///./scim.db", echo=True)

# Create all tables
def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    
    with Session(engine) as session:
        # give session to any endpoint that depends on it
        yield session
    
    # close session after the request ends


