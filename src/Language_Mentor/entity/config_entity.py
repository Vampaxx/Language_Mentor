from pathlib import Path
from typing import Optional

from typing import List, Dict,Union
from pydantic import BaseModel,Field

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelConfig:
    Model_name              : str 
    temperature             : int 
    api_key                 : Optional[str]


class QuestionsModel(BaseModel):
    questions   : List[str] = Field(description="5 questions to know the language proficiency of user.")


class ActivityExample(BaseModel):
    """Model to represent an example of an activity."""
    title               : str       = Field(description="Title of the example")
    description         : str       = Field(description="Description of the example")
    activity_examples   : List[str] = Field(description="List of activity examples related to this example")

class Subtopic(BaseModel):
    """Model to represent a subtopic within a chapter."""
    title   : str                   = Field(description="Title of the subtopic")
    summary : str                   = Field(description="Summary of the subtopic")
    examples: List[ActivityExample] = Field(description="List of examples for this subtopic")

class Chapter(BaseModel):
    """Model to represent a chapter."""
    title       : str               = Field(description="Title of the chapter")
    summary     : str               = Field(description="Summary of the chapter")
    subtopics   : List[Subtopic]    = Field(description="List of subtopics covered in this chapter")

class ExamQuestionAndAnswer(BaseModel):
    questions   : List[str]         = Field(default_factory=list,
                                            description="A list of 5 questions to assess the language proficiency of the user.")
    #answers     : Dict[str, str]    = Field(default_factory=dict,
     #                                       description="A dictionary of questions as keys and their respective answers as values.")

class AnswerEvaluation(BaseModel):
    score: str = Field(description="Total marks obtained based on correct answers")