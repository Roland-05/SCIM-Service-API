from sqlmodel import Field, SQLModel, Session, create_engine




engine = create_engine("sqlite:///./scim.db")

SQLModel.metadata.create_all(engine)



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


