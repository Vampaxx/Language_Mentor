# Language Curriculum Chatbot

The Language Curriculum Chatbot is a Flask-based web application designed to guide users through language learning. This chatbot dynamically adjusts the language curriculum based on user responses and scores, moving users through proficiency levels—Beginner, Intermediate, and Advanced—and provides a certificate upon successful completion.

## Features

- **Language Selection**: Users can choose a language to begin learning.
- **Dynamic Curriculum Progression**: The curriculum adapts to user responses, helping them progress through language levels.
- **Examinations**: Users take exams at the end of each level. Passing moves them to the next level; failing prompts a repeat.
- **Certification**: Upon passing the Advanced level exam, users are awarded a completion certificate.

## Installation

Follow these steps to set up and run the application locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Vampaxx/Language_Mentor
cd Language_Mentor
```

### 3. Install the Required Dependencies

Make sure you have Python and pip installed. Then install the required dependencies:

```bash

pip install -r requirements.txt
```
### Usage

Run the Flask Application:

Start the application by executing:

```bash

python main.py
```
## DEMO WORKING 

Access the Web Interface

Open your browser and go to http://127.0.0.1:5000/ to start using the chatbot.
Usage
Step-by-Step Guide

  1. Select a Language: Start by choosing a language for your curriculum.
  2. Answer Questions: The chatbot will assess your current language level through questions.
  3. View Curriculum: Based on your level, the chatbot generates a curriculum with relevant materials.
  4. Take Exams: At the end of each level, take an exam. A passing score allows progression to the next level.
  5. Receive a Certificate: After passing the Advanced level exam, you will receive a congratulatory certificate.

Project Structure

  - main.py: Main Flask application file with routes, session management, and chatbot logic.
  - Language_Mentor/: Directory containing configurations, logging, and chatbot models.
  - templates/: Contains HTML templates for different pages (language selection, question flow, curriculum, exam, and certificate page).

Project Summary

The Language Curriculum Chatbot application streamlines the process of language learning by using interactive questions and adaptive progression. It allows users to select a language, answer questions to determine proficiency, and then work through a curriculum tailored to their level. This guided learning path is capped by exams that must be passed to advance to the next level, ultimately leading to a certificate of completion.

### Approach to Development

  - Application Setup: Organized the project with separate components for model configurations, data handling, and user interface.
  - User Progress Tracking: Designed session-based tracking to monitor user responses and advancement through levels.
  - Dynamic Curriculum Adjustment: Integrated logic for assessing answers and dynamically updating the curriculum.
  - Flask Web Interface: Built a clear and user-friendly interface for ease of navigation and user engagement.
  - Testing and Validation: Validated the chatbot with sample questions to ensure it correctly classifies levels and generates curriculum.
