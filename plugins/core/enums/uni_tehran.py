from enum import Enum


class SearchType(Enum):
    Profile = "profile"
    Retired = "retired"
    Decedent = "decedent"
    Journals = "journals"
    Publications = "publications"
    Prizes = "prizes"


class ElectricalComputerEngineeringInfoFields(Enum):
    Degree = 0
    Major = 1
    PhoneNumber = 2
    Email = 3
