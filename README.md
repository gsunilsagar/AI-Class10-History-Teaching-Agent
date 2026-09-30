# Class 10 History AI Teaching Assistant

## 1. Introduction

The Class 10 History AI Teaching Assistant is an AI-powered educational
application designed to help Class 10 students learn History.

The application combines:

- HTML
- CSS
- JavaScript
- Python
- Hugging Face LLM
- Markdown-based subject context

The system is designed to act as a teaching assistant rather than a
generic chatbot.

---

## 2. Features

The system can:

- Answer Class 10 History questions.
- Explain historical concepts in simple language.
- Explain causes and consequences.
- Provide step-by-step explanations.
- Help with examination questions.
- Correct misconceptions.
- Encourage student participation.
- Use a subject-specific History context file.
- Communicate with an LLM through Hugging Face.

---

## 3. System Architecture

```text
                    STUDENT
                       |
                       v
              +----------------+
              |   FRONTEND     |
              | HTML/CSS/JS    |
              +-------+--------+
                      |
                    HTTP
                      |
                      v
              +----------------+
              |    PYTHON      |
              |    BACKEND     |
              +-------+--------+
                      |
              +-------+--------+
              |                |
              v                v
      +---------------+  +-------------+
      | history_      |  | Hugging     |
      | context.md    |  | Face LLM    |
      +---------------+  +------+------+
                              |
                              v
                       AI TEACHING
                         RESPONSE
                              |
                              v
                           STUDENT