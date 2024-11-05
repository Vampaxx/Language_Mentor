from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)

language_curriculum = {
    "chapters": [
        {
            "title": "Chapter 1: Basic Foundations",
            "summary": "This chapter covers the basics of the English language, including numbers, alphabet, and common words.",
            "subtopics": [
                {
                    "title": "Numbers 1-10",
                    "summary": "Learn the numbers from 1 to 10 in English.",
                    "examples": [
                        {
                            "title": "Counting Objects",
                            "description": "Practice counting objects using numbers 1-10.",
                            "activity_examples": ["One apple.", "Two dogs.", "Three books."]
                        },
                        {
                            "title": "Number Spelling",
                            "description": "Learn the spelling of numbers 1-10.",
                            "activity_examples": ["One - O-N-E", "Two - T-W-O", "Three - T-H-R-E-E"]
                        }
                    ]
                },
                {
                    "title": "Alphabet",
                    "summary": "Learn the 26 letters of the English alphabet.",
                    "examples": [
                        {
                            "title": "Uppercase Letters",
                            "description": "Practice writing uppercase letters.",
                            "activity_examples": ["A", "B", "C", "D", "E"]
                        },
                        {
                            "title": "Lowercase Letters",
                            "description": "Practice writing lowercase letters.",
                            "activity_examples": ["a", "b", "c", "d", "e"]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Chapter 2: Common Words",
            "summary": "This chapter introduces common words and their spellings in English.",
            "subtopics": [
                {
                    "title": "Food Words",
                    "summary": "Learn common food-related words.",
                    "examples": [
                        {
                            "title": "Fruit Words",
                            "description": "Practice spelling fruit words.",
                            "activity_examples": ["Apple - A-P-P-L-E", "Banana - B-A-N-A-N-A", "Orange - O-R-A-N-G-E"]
                        },
                        {
                            "title": "Drink Words",
                            "description": "Practice spelling drink words.",
                            "activity_examples": ["Water - W-A-T-E-R", "Tea - T-E-A", "Coffee - C-O-F-F-E-E"]
                        }
                    ]
                }
            ]
        }
    ]
}

proficiency_level = "beginner"

@app.route("/")
def home():
    return render_template("rough.html",proficiency_level=proficiency_level, language_curriculum=language_curriculum)


if __name__ == "__main__":
    app.run(debug=True)
