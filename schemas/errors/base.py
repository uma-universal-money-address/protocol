from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel


class ErrorDefinition(BaseModel):
    code: str
    httpStatusCode: int
    description: str


class ErrorList(BaseModel):
    errors: List[ErrorDefinition]


class ErrorGenerator(ABC):
    @abstractmethod
    def generate(self, errorList: ErrorList) -> str:
        pass

    @abstractmethod
    def get_output_directory(self) -> str:
        pass

    @abstractmethod
    def get_output_file_name(self) -> str:
        pass
