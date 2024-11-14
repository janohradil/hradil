from sqlmodel import Field, Session, SQLModel, create_engine, select

class Odpoved(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    meno: str
    priezvisko: str
    telefon: str
    sprava: str

