from pydantic import BaseModel


class Get_max_duration(BaseModel):
    title_name: str
    release_year: int
    duration: int
    duration_unit: str
    service_name: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "title_name": "Ncis",
                "release_year": 2017,
                "duration": 1,
                "duration_unit": "Season",
                "service_name": "Netflix"
            }
        }


class Get_count_platform(BaseModel):
    type: str
    amount: int
    service_name: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": [
                {
                    "type": "Movie",
                    "amount": 1484,
                    "service_name": "Hulu"
                },
                {
                    "type": "Serie",
                    "amount": 1589,
                    "service_name": "Hulu"
                }
            ]
        }


class Get_most_frequent_listedin(BaseModel):
    listed_in: str
    amount: int
    service_name: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "listed_in": "Comedy",
                "amount": 2652,
                "service_name": "Netflix"
            }
        }


class Get_actor(BaseModel):
    actor: str
    amount: int
    release_year: int
    service_name: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "actor": "Vincent Tong",
                "amount": 8,
                "release_year": 2019,
                "service_name": "Netflix"
            }
        }


class Get_listed_in(BaseModel):
    listed_in: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "listed_in": [
                    "Action",
                    "Adult",
                    "Adventure",
                    "Animals",
                    "etc",
                    "etc",
                    "etc",
                ]
            }
        }
