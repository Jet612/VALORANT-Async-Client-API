from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

@dataclass
class httpStatusError:
    httpStatus: int
    errorCode: str
    message: str