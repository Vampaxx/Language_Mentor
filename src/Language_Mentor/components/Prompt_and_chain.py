
from typing import List, Dict
from pydantic import BaseModel

from Language_Mentor import logger 
from Language_Mentor.utils.common import *
from Language_Mentor.components.Model import ModelSetup
from Language_Mentor.config.configuration import ConfigurationManager
from Language_Mentor.entity.config_entity import (ModelConfig,
                                                   Chapter,QuestionsModel,ExamQuestionAndAnswer,AnswerEvaluation)#,Curriculum,CurriculumFilter)

from langchain_core.runnables import RunnablePassthrough,RunnableLambda
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers.json import JsonOutputParser
from langchain.output_parsers import PydanticOutputParser





class PromptAndChain(ModelSetup):

    def __init__(self,model_config  : ModelConfig,):
        super().__init__(model_config)
        self.llm                        = self.model_setup()


    def question_prompt(self): 
        logger.info(f"Question Prompting and chain has started....")
        question_prompt = """
            You are an expert in linguistics.
            Create 5 questions to know the {language} proficiency of user. The created questions should be in {language}.
            Each question should evaluate the user’s understanding of grammar, sentence structure, and vocabulary.
            The questions should help to determine whether the user’s proficiency level is beginner, intermediate, or advanced.
            Only create this 5 questions only.And strictily follows the JSON Format. 

            Your output should be in JSON format, structured using the following classes:
            ```python 
            class QuestionsModel(BaseModel):
                questions   : List[str] = Field(description="5 questions to know the language proficiency of user.")
            strictily stick to this format.
            """
        question_template = PromptTemplate(template       = question_prompt,
                                           input_variable = ["language"],)
                                           #partial_variable = {"k":"1"})
        chain = (
            {
                "language"  : RunnablePassthrough(),
            }
            | question_template 
            | self.llm
            | JsonOutputParser(pydantic_object=QuestionsModel)
        )
        logger.info("question prompt is completed.")
        return chain 
    

    def proficiency_level_prompt(self):
        logger.info(f"Profiency level Prompting and chain has started....")
        profiency_level_prompt = """
            You are an expert in linguistics.
            Your role is to closely analyze the provided {text}, which contains questions and user responses.
            Based on your analysis, determine the user's language proficiency level. Only return one of the following levels: 'Beginner', 'Intermediate', or 'Advanced'.
            Do not respond with more than one word
            """
        question_template = PromptTemplate(template       = profiency_level_prompt,
                                           input_variable = ["text"],)
        
        self.proficiency_chain = (
            {
                "text"  : RunnablePassthrough(),
            }
            | question_template 
            | self.llm
            | StrOutputParser()
        )
        logger.info("Proficiency level prompt is completed.")
        return self.proficiency_chain 
    

    def language_curriculum_prompt(self):
        logger.info(f"Language curriculum prompting has started....")
        language_level_prompt   = """
    You are a linguistics expert in {language}. Your task is to design an {language} language curriculum tailored to the user’s {language_level} proficiency.
    The curriculum should be structured in 3 chapters with each chapter containing 5 examples for clear understanding and practice. The content for each level should be as follows:
    Only create chapter of {language_level} level.
    The curriculum structure based on {language_level} is as follows:
    
    Beginner Level:
        Chapter 1: Teach basic numbers (e.g., one, two, three, etc.) and the alphabet.
        Chapter 2: Introduce common words and their spellings.
        Chapter 3: Teach basic phrases to help the user form simple sentences.

    Intermediate Level:
        Chapter 1: Cover essential parts of speech, including nouns, verbs, and pronouns.
        Chapter 2: Teach adjectives, adverbs, conjunctions, interjections, and prepositions.
        Chapter 3: Introduce different sentence structures to improve sentence formation skills.

    Advanced Level:
        Chapter 1: Teach phrasal verbs and their meanings.
        Chapter 2: Explore word formation techniques.
        Chapter 3: Teach how to use formal and informal language in various contexts.

    Each chapter should include practical examples to reinforce understanding and help the user progress confidently through the curriculum.
    Your output should be in JSON format, structured using the following classes:
    ```python 
    class ActivityExample(BaseModel):
        "Model to represent an example of an activity."
        title               : str       = Field(description="Title of the example")
        description         : str       = Field(description="Description of the example")
        activity_examples   : List[str] = Field(description="List of activity examples related to this example")

    class Subtopic(BaseModel):
        "Model to represent a subtopic within a chapter."
        title   : str                   = Field(description="Title of the subtopic")
        summary : str                   = Field(description="Summary of the subtopic")
        examples: List[ActivityExample] = Field(description="List of examples for this subtopic")

    class Chapter(BaseModel):
        "Model to represent a chapter."
        title       : str               = Field(description="Title of the chapter")
        summary     : str               = Field(description="Summary of the chapter")
        subtopics   : List[Subtopic]    = Field(description="List of subtopics covered in this chapter")
        """
        language_curriculum_template = PromptTemplate(template          = language_level_prompt,
                                                      input_variable    = ["language_level","language"])
        
        self.language_curriculum_chain = (
            {
                "language_level"    : RunnablePassthrough(),
                "language"          : RunnablePassthrough()
            }
            | language_curriculum_template 
            | self.llm
            | JsonOutputParser(pydantic_object=Chapter)
        )
        logger.info("Language curriculum prompting has completed.")
        return self.language_curriculum_chain 

    
    def exam_prompt(self):
        logger.info(f"Examination Prompting and chain has started....")
        profiency_level_prompt = """
        As an expert in crafting examination questions, create a set of 5 meaningful simple questions to assess the user's understanding of the provided {curriculum} of {language} Language. 
        Structure each question following the format specified below. Ensure that the questions cover a range of topics within the curriculum to provide a thorough assessment.
        The output should be in JSON format, structured as a dictionary with a single key "question", and the value should be a list containing 5 questions. Example format:
        {{"question": ["question1","question2"....,"Question5"]}}
        """
        #
        #{{"question": ["question1","question2",..."question10"]}}
        question_template = PromptTemplate(template       = profiency_level_prompt,
                                           input_variable = ["curriculum","language"],)
        
        self.proficiency_chain = (
            {
                "curriculum"    : RunnablePassthrough(),
                "language"      : RunnablePassthrough()
            }
            | question_template 
            | self.llm
            | JsonOutputParser(pydantic_object=ExamQuestionAndAnswer)
        )
        logger.info("Examination Prompting and chain completed.")
        return self.proficiency_chain                
    
    
    def evaluation_prompt(self):
        logger.info(f"Evaluation Prompting and chain has started....")
        evaluation_prompt = """
        As an expert evaluator, your task is to assess a question and its respective response provided in the following format.

        Each key-value pair represents a question (key) and the student's response (value). For example, "What is the English word for the number 5?": "five", where "What is the English word for the number 5?" is the question (key), and "five" is the student's answer (value).

        Task Details:

            Analyze each question and its corresponding student response carefully.

            Assign a score of 1 for each correct answer and a score of 0 for each incorrect answer.

            Sum up the correct answers and return the total score as a JSON object in the following format:
            {{"score":total_score}}
            
        The Question and Answer is : 
        {question_and_answer}
    """
        
        parser              = JsonOutputParser(pydantic_object=AnswerEvaluation)
        evaluation_template = PromptTemplate(template           = evaluation_prompt,
                                           input_variable       = ["question_and_answer"],
                                           partial_variables    = {"format_instructions": parser.get_format_instructions()})
        
        
        self.proficiency_chain = (
            {
                "question_and_answer"  : RunnablePassthrough(),
            }
            | evaluation_template 
            | self.llm
            | parser
        )
        logger.info("Evaluation Prompting and chain completed.")
        return self.proficiency_chain                




if __name__ == "__main__":
    manager             = ConfigurationManager()
    model_config        = manager.get_model_config()
    prompt_and_chain    = PromptAndChain(model_config=model_config)
    chain                       = prompt_and_chain.question_prompt()
    level_chain                 = prompt_and_chain.proficiency_level_prompt()
    language_curriculum_chain   = prompt_and_chain.language_curriculum_prompt()
    examination_chain           = prompt_and_chain.exam_prompt() 
    evaluation_chain            = prompt_and_chain.evaluation_prompt()



    question_res = {
                    'Write the next number in the sequence: One, Two, Three...': 'four',
                    'What is the English word for the number 5?': 'five', 
                    "What is the first letter of the word 'Apple'?": 'P', 
                    }
    
    #print(chain.invoke("english"))
    proficiency_level   = level_chain.invoke("question : Choose the correct sentence structure: 'If I __________ (to study) harder, I would have passed the exam.' a) study b) studied c) had studied d) would study and user_response : c. question : Identify the correct form of the possessive adjective in the following sentence: '______ car is red.' a) My b) Mine c) I d) Me and user_response : a. question : What does the phrase 'break a leg' mean in informal English? a) To injure oneself. b) To wish someone good luck. c) To take a risk. d) To be very tired. and user_response : b. question : What is the meaning of the word 'fastidious' in the following sentence: 'She is a fastidious editor.'? a) Careless. b) Meticulous. c) Quick. d) Lazy. and user_response : b. question : Which of the following sentences is in the passive voice? a) The dog bites the man. b) The man was bitten by the dog. c) The dog is biting the man. d) The man bites the dog. and user_response : b")
    """language_curriculum = language_curriculum_chain.invoke({"language_level"    : proficiency_level,
                                                            "language"          : "english"})"""
    print(proficiency_level)
    #print((json_to_sentence(language_curriculum)))
    mark = evaluation_chain.invoke(json_to_sentence(question_res))
    print(mark)
    #exam_ques_and_ans   = examination_chain.invoke(json_to_sentence(language_curriculum)) 
    #print(len(exam_ques_and_ans['question']))
    #print(language_curriculum.get("chapters"))
    #print(language_curriculum)
    