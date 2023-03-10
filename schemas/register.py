from pydantic import BaseModel


class RegisterSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
