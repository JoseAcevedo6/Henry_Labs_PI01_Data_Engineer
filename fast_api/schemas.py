from pydantic import BaseModel


class Actor(BaseModel):
    id_actor: int
    actor: str

    class Config:
        orm_mode = True


class Listed_in(BaseModel):
    id_listed_in: int
    listed_in: str

    class Config:
        orm_mode = True


class Service(BaseModel):
    id_service: int
    service: str

    class Config:
        orm_mode = True


class Title(BaseModel):
    id_title: int
    title: str
    release_year: int
    duration_time: int
    duration_unit: str

    class Config:
        orm_mode = True


class Title_actor(BaseModel):
    id_title: int
    id_actor: int

    class Config:
        orm_mode = True


class Title_listed_in(BaseModel):
    id_title: int
    id_listed_in: int

    class Config:
        orm_mode = True


class Title_service(BaseModel):
    id_title: int
    id_service: int

    class Config:
        orm_mode = True
