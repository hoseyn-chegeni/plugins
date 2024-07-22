from abc import ABC, abstractmethod

from schemas import Employee, Professor

class University(ABC):

    @abstractmethod
    def get_professor_page(self) -> Professor:
        pass

    @abstractmethod
    def get_employee_page(self) -> Employee:
        pass