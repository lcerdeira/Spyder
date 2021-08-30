from typing import List
from pydantic import BaseModel
from enum import Enum

class Organisms(str, Enum):
    sequi = 'sequi'
    klepn = 'klepn'
    ngonorrhoeae = 'ngonorrhoeae'
    styphi = 'styphi'
    rensm_rensm = 'rensm-rensm'
    saureus = 'saureus'
    zikv = 'zikv'

class Collection(BaseModel):
    path: str
    filename: str

class Collections(BaseModel):
    organism: str
    path: List[Collection]
