from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Union


class Activity(BaseModel):
    description: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    title: Optional[str] = None


class Article(BaseModel):
    authors: List[str] = []
    date: Optional[str] = None
    details: Optional[str] = None
    link: Optional[str] = None
    title: Optional[str] = None


class Book(BaseModel):
    authors: List[str] = []
    copy_num: Optional[Union[int, str]] = None
    place: Optional[str] = None
    publish_date: Optional[str] = None
    title: Optional[str] = None


class Course(BaseModel):
    description: Optional[str] = None
    grade: Optional[str] = None
    period: Optional[str] = None
    title: Optional[str] = None


class Editor(BaseModel):
    description: Optional[str] = None
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


class JobExperience(BaseModel):
    end_date: Optional[str] = None
    place: Optional[str] = None
    start_date: Optional[str] = None
    title: Optional[str] = None


class Language(BaseModel):
    language: Optional[str] = None
    speaking: Optional[str] = None
    translate: Optional[str] = None


class Membership(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class Mentor(BaseModel):
    end_date: Optional[str] = None
    period: Optional[str] = None
    place: Optional[str] = None
    student: Optional[str] = None
    title: Optional[str] = None


class ResearchPlan(BaseModel):
    end_date: Optional[str] = None
    executives: List[str] = None
    place: Optional[str] = None
    sponser: Optional[str] = None
    status: Optional[str] = None
    title: Optional[str] = None


class ScientificChair(BaseModel):
    date: Optional[str] = None
    details: Optional[str] = None
    related_people: List[str] = []
    title: Optional[str] = None


class ScientificReport(BaseModel):
    authors: List[str] = []
    date: Optional[str] = None
    organization: Optional[str] = None
    partners: List[str] = []
    subject: Optional[str] = None
    title: Optional[str] = None


class Skill(BaseModel):
    title: Optional[str] = None
    start_date: Optional[str] = None


class Social(BaseModel):
    google: Optional[str] = None
    linkedin: Optional[str] = None
    orcid: Optional[str] = None
    researchgate: Optional[str] = None
    scholar: Optional[str] = None
    scimet: Optional[str] = None
    scopus: Optional[str] = None
    telegram: Optional[str] = None
    twitter: Optional[str] = None
    webofscience: Optional[str] = None
    website: Optional[str] = None
    personal_cv: Optional[str] = None


class Thesis(BaseModel):
    authors: List[str] = []
    defense_date: Optional[str] = None
    title: Optional[str] = None


class TransferringKnowledge(BaseModel):
    date: Optional[str] = None
    place: Optional[str] = None
    title: Optional[str] = None


class Workshop(BaseModel):
    event_date: Optional[str] = None
    event_place: Optional[str] = None
    organizing: Optional[str] = None
    title: Optional[str] = None


class Professor(BaseModel):
    model_config = ConfigDict(extra="allow")

    activities: List[Activity] = []
    article_in_print: List[Union[str, Article]] = []
    biography: Optional[str] = None
    books: List[Book] = []
    conference_editors: List[Editor] = []
    conference_papers: List[Union[str, Article]] = []
    courses: List[Course] = []
    doctoral_thesis: List[Thesis] = []
    educational_records: List[EducationalRecord] = []
    email: List[str] = []
    faculty: Optional[str] = None
    full_name: Optional[str] = None
    full_name_en: Optional[str] = None
    group: Optional[str] = None
    college: Optional[str] = None
    h_index: Optional[str] = None
    honors: List[Honor] = []
    image: Optional[str] = None
    interests: List[Interest] = []
    inventions: List[Invention] = []
    job_experiences: List[JobExperience] = []
    journal_articles: List[Union[str, Article]] = []
    journal_editors: List[Editor] = []
    languages: List[Language] = []
    magazines_membership: List[Membership] = []
    masters_thesis: List[Thesis] = []
    non_professional_activities: List[Activity] = []
    other_activities: List[Activity] = []
    phone_number: Optional[str] = None
    professional_membership: List[Membership] = []
    projects: List[str] = []
    rank: Optional[str] = None
    references: Optional[str] = None
    research_laboratories: List[str] = []
    research_plans: List[ResearchPlan] = []
    responsibilities: List[str] = []
    scientific_chair: List[ScientificChair] = []
    scientific_report: List[ScientificReport] = []
    skills: List[Skill] = []
    socials: Social = Social()
    student_advisors: List[Mentor] = []
    student_mentors: List[Mentor] = []
    student_projects: List[str] = []
    transferring_knowledge: List[TransferringKnowledge] = []
    university_link: str = None
    workshops: List[Workshop] = []
