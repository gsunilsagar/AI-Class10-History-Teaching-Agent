# Project Plan

## Project Title

Class 10 History AI Teaching Assistant

---

## 1. Project Objective

The objective of this project is to develop an AI-powered teaching
assistant that helps Class 10 students learn History.

The system uses a Large Language Model together with a subject-specific
History context file.

The assistant is designed to behave like a teaching assistant rather
than a generic chatbot.

---

## 2. Target Users

The primary users are Class 10 students studying History.

---

## 3. Technologies

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python 3.8.4
- Python HTTP server
- JSON API

### AI

- Hugging Face Inference API
- HuggingFaceH4/zephyr-7b-beta

### Context

- Markdown file
- history_context.md

### Configuration

- .env
- python-dotenv

---

## 4. Development Plan

### Phase 1 – Project Setup

Create the project folders and files.

### Phase 2 – AI Integration

Connect Python to the Hugging Face API.

### Phase 3 – Teaching Context

Create a History-specific Markdown context file.

### Phase 4 – Backend

Create a Python backend that:

1. Receives student questions.
2. Loads the History context.
3. Builds a teaching prompt.
4. Sends the prompt to the LLM.
5. Returns the generated answer.

### Phase 5 – Frontend

Create a web interface using:

- HTML
- CSS
- JavaScript

### Phase 6 – Integration

Connect:

Frontend → Backend → Context → Hugging Face LLM

### Phase 7 – Testing

Test:

- History questions
- Explanations
- Exam questions
- Incorrect student statements
- Questions outside History

### Phase 8 – Documentation

Complete:

- README
- Project plan
- Architecture diagram
- Demonstration screenshots

---

## 5. Expected Result

The final system should allow a student to ask a Class 10 History
question and receive a clear, step-by-step, educational response.

The system should use the History context file and follow the teaching
instructions contained within it.