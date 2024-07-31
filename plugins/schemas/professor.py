from pydantic import BaseModel
from typing import List, Optional


class Social(BaseModel):
    google: Optional[str] = None
    linkedin: Optional[str] = None
    orcid: Optional[str] = None
    researchgate: Optional[str] = None
    scholar: Optional[str] = None
    scopus: Optional[str] = None
    telegram: Optional[str] = None
    twitter: Optional[str] = None
    webofscience: Optional[str] = None
    personal_cv: Optional[str] = None


class Activity(BaseModel):
    description: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    title: Optional[str] = None


class Book(BaseModel):
    authors: List[str] = []
    copy_num: Optional[int] = None
    place: Optional[str] = None
    publish_date: Optional[str] = None
    title: Optional[str] = None


class Course(BaseModel):
    description: Optional[str] = None
    period: Optional[str] = None
    title: Optional[str] = None


class EducationalRecord(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None
    degree: Optional[str] = None
    graduation_date: Optional[str] = None
    study_field: Optional[str] = None
    title: Optional[str] = None
    university: Optional[str] = None


class Honor(BaseModel):
    title: Optional[str] = None
    date: Optional[str] = None


class Interest(BaseModel):
    start_date: Optional[str] = None
    title: Optional[str] = None


class Invention(BaseModel):
    country: Optional[str] = None
    expiration_date: Optional[str] = None
    partners: List[str] = []
    registration_date: Optional[str] = None
    registration_number: Optional[str] = None
    title: Optional[str] = None


class Language(BaseModel):
    language: Optional[str] = None
    speaking: Optional[str] = None
    translate: Optional[str] = None


class Membership(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class Thesis(BaseModel):
    authors: List[str] = []
    defense_date: Optional[str] = None
    title: Optional[str] = None


class Skill(BaseModel):
    title: Optional[str] = None
    start_date: Optional[str] = None


class Workshop(BaseModel):
    event_date: Optional[str] = None
    event_place: Optional[str] = None
    organizing: Optional[str] = None
    title: Optional[str] = None


class Professor(BaseModel):
    activities: List[Activity] = []
    books: List[Book] = []
    college: Optional[str] = None
    conference_papers: List[str] = []
    courses: List[Course] = []
    doctoral_thesis: List[Thesis] = []
    educational_records: List[EducationalRecord] = []
    email: Optional[str] = None
    full_name: Optional[str] = None
    full_name_en: Optional[str] = None
    group: Optional[str] = None
    h_index: Optional[str] = None
    honors: List[Honor] = []
    image: Optional[str] = None
    interests: List[Interest] = []
    inventions: List[Invention] = []
    journal_articles: List[str] = []
    languages: List[Language] = []
    magazines_membership: List[Membership] = []
    masters_thesis: List[Thesis] = []
    phone_number: Optional[str] = None
    professional_membership: List[Membership] = []
    projects: List[str] = []
    rank: Optional[str] = None
    references: Optional[str] = None
    research_laboratories: List[str] = []
    responsibilities: List[str] = []
    skills: List[Skill] = []
    socials: Social = Social()
    student_projects: List[str] = []
    university_link: str = None
    workshops: List[Workshop] = []
