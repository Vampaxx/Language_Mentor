from Language_Mentor import logger
from Language_Mentor.components.Model import ModelSetup
from Language_Mentor.utils.common import json_to_sentence
from Language_Mentor.config.configuration import ConfigurationManager
from Language_Mentor.components.Prompt_and_chain import PromptAndChain




from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)
app.secret_key = 'your_secret_keys'  

manager         = ConfigurationManager()
model_config    = manager.get_model_config()
llm             = ModelSetup(config=model_config).model_setup()
prompt_and_chain= PromptAndChain(model_config=model_config)
language_level  = ['Beginner', 'Intermediate','Advanced']
##---------------------------Chain-----------------------------## 
question_chain              = prompt_and_chain.question_prompt()
level_chain                 = prompt_and_chain.proficiency_level_prompt()
language_curriculum_chain   = prompt_and_chain.language_curriculum_prompt()
examination_chain           = prompt_and_chain.exam_prompt() 
## -------------------------Evaluation----------------------------## 
evaluation_chain            = prompt_and_chain.evaluation_prompt()



@app.before_request
def before_request():
    """Initialize session variables before each request."""
    if 'question_index' not in session:
        session['question_index']       = 0
    if 'question_and_response' not in session:
        session['question_and_response'] = {}
    if 'questions' not in session:
        session['questions']    = []
    if "language_curriculum" not in session:
        session["language_curriculum"] = []



@app.route("/", methods=["GET", "POST"])
def question_flow():
    """Handles question flow and user responses based on language selection."""
    logger.info("Question flow initialized...")
    if not session['questions']:
        if request.method == "POST":
            language    = request.form.get("language")
            if language:
                questions_dict                      = question_chain.invoke(language)  # Initialize questions based on language
                session['questions']                = questions_dict['questions']
                session['question_index']           = 0
                session['question_and_response']    = {}
                session['selected_language']        = language
                logger.info(f"Questions initialized for language: {language}")
                return redirect(url_for("question_flow"))
            else:
                return "Language selection is required to proceed.", 400
        else:
            return render_template("language_selection.html")  

    questions               = session.get('questions', [])
    question_index          = session.get('question_index', 0)
    question_and_response   = session.get('question_and_response', {})
    
    if question_index >= len(questions):
        return redirect(url_for("curriculum"))

    if request.method == "POST":
        user_response                                       = request.form.get("user_response")
        question_and_response[questions[question_index]]    = user_response
        session['question_and_response']                    = question_and_response  

        question_index             += 1
        session['question_index']   = question_index  

        if question_index >= len(questions):
            return redirect(url_for("curriculum"))
    current_question    = questions[question_index]
    logger.info(f"Displaying question {question_index + 1}")
    return render_template("index.html", question=current_question, question_index=question_index + 1)



@app.route("/curriculum")
def curriculum():
    logger.info("Language curriculum initialized...")
    question_and_response   = session.get('question_and_response', {})
    selected_language       = session.get('selected_language', 'Unknown Language')
    
    level_chain                 = prompt_and_chain.proficiency_level_prompt()
    language_curriculum_chain   = prompt_and_chain.language_curriculum_prompt()
    if not isinstance(question_and_response, dict):
        question_and_response   = {}
    question_response           = ". ".join([f"question: {key} and user_response: {value}" for key, value in question_and_response.items()])
    ## chain## 
    proficiency_level           = level_chain.invoke(question_response)
    language_curriculum         = language_curriculum_chain.invoke({"language_level"    : proficiency_level,
                                                                    "language"          : selected_language})
    print(proficiency_level) 
    session["language_curriculum"]  = language_curriculum

    session.pop('question_index', None)
    logger.info("question_index removed from session.")
    session.pop('question_and_response', None)
    logger.info("question_and_response removed from session.")
    session.pop("questions", None)
    logger.info("questions removed from session.")

    print(proficiency_level,selected_language)
    logger.info("Completed.")
    return render_template("curriculum.html",proficiency_level=proficiency_level, language_curriculum=language_curriculum)




@app.route("/exam_page", methods=["GET", "POST"])
def exam_page():
    if request.method == "GET":
        logger.info("Examination initialized...")
        
        selected_language                   = session.get('selected_language', 'Unknown Language')
        language_curriculum                 = session.get("language_curriculum")
        exam_questions                      = examination_chain.invoke({"curriculum": json_to_sentence(language_curriculum),
                                                                        "language"  : selected_language})
        
        if exam_questions:
            session["questions"]                = exam_questions.get("question", [])
            session["question_index"]           = 0
            session["question_and_response"]    = {}

            questions               = session.get("questions", [])
            question_index          = session.get("question_index", 0)
            question_and_response   = session.get("question_and_response", {})

            current_question        = questions[question_index]

            return render_template("exam_question.html",question=current_question, question_index=question_index + 1)
        else:
            return "Language Curriculum is required to process",400
    
    questions               = session.get("questions", [])
    question_index          = session.get("question_index", 0)
    question_and_response   = session.get("question_and_response", {})

    if question_index >= len(questions):
        print("All questions answered.")
        

        #print(question_and_response)
        mark                = evaluation_chain.invoke(json_to_sentence(question_and_response))
        print(mark)
        return redirect(url_for("question_flow"))
       
    if request.method == "POST":
        user_response                                       = request.form.get("user_response")
        question_and_response[questions[question_index]]    = user_response
        session["question_and_response"]                    = question_and_response

        question_index             += 1
        session["question_index"]   = question_index

        if question_index >= len(questions):
            print("All questions and answers:")
            print(question_and_response)
            mark                    = evaluation_chain.invoke(json_to_sentence(question_and_response))
            print(mark)
            return redirect(url_for("question_flow"))
    
    current_question = questions[question_index]
    print(current_question,question_index)
    return render_template("exam_question.html", question=current_question, question_index=question_index + 1)





if __name__ == "__main__":
    app.run(debug=True)