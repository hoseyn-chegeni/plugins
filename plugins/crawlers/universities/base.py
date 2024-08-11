from abc import ABC, abstractmethod
from schemas.professor import Professor
from schemas.employee import Employee


class University(ABC):

    @abstractmethod
    def get_professor_page(self) -> Professor:
        pass

    @abstractmethod
    def get_employee_page(self) -> Employee:
        pass
