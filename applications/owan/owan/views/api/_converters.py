from pydantic import BaseModel


class Health(BaseModel):
    health: str


class PredictionRequestResponse(BaseModel):
    recieved_file: str
