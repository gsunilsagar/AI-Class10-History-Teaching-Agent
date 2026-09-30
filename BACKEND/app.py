import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise RuntimeError(
        "HF_TOKEN was not found. Please check your .env file."
    )

# This is the model that you already successfully tested.
MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONTEXT_FILE = os.path.join(
    PROJECT_ROOT,
    "CONTEXT",
    "history_context.md"
)

FRONTEND_FOLDER = os.path.join(
    PROJECT_ROOT,
    "FRONTEND"
)


# ============================================================
# LOAD HISTORY CONTEXT
# ============================================================

def load_history_context():
    """Load the teaching knowledge and instructions."""

    if not os.path.exists(CONTEXT_FILE):
        return (
            "No history context file was found. "
            "Answer only using general Class 10 History knowledge."
        )

    with open(CONTEXT_FILE, "r", encoding="utf-8") as file:
        return file.read()


# ============================================================
# HUGGING FACE CLIENT
# ============================================================

client = InferenceClient(
    token=HF_TOKEN
)


# ============================================================
# CREATE TEACHING PROMPT
# ============================================================

def create_messages(student_question):
    """Create the system and user messages for the teaching agent."""

    history_context = load_history_context()

    system_prompt = """
You are a Class 10 History Teaching Assistant.

You are NOT a generic chatbot.

Your primary purpose is to teach Class 10 History students.

Use the provided HISTORY TEACHING CONTEXT as your main instructional
knowledge and teaching guidance.

Important rules:

1. Explain concepts in simple Class 10 level language.
2. Teach step by step.
3. Explain causes, events and consequences clearly.
4. When useful, give examples.
5. Encourage the student to think rather than simply giving answers.
6. For homework or exam questions, help the student understand how to
   construct the answer.
7. If appropriate, give a hint before giving a complete answer.
8. Correct historical misunderstandings politely.
9. Do not invent dates, people, quotations or historical facts.
10. Stay focused on Class 10 History.
11. Keep answers reasonably concise unless the student asks for detail.
12. Use headings and numbered points when they improve understanding.
13. If the student asks a question outside History, politely explain that
    you are designed primarily to teach Class 10 History.
14. Maintain a friendly, patient and encouraging teacher-like tone.

HISTORY TEACHING CONTEXT:

""" + history_context

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": student_question
        }
    ]

    return messages


# ============================================================
# ASK AI
# ============================================================

def ask_ai(student_question):
    """Send the student's question to Hugging Face."""

    messages = create_messages(student_question)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=500,
        temperature=0.4
    )

    answer = response.choices[0].message.content

    return answer


# ============================================================
# HTTP SERVER
# ============================================================

class TeachingAgentHandler(BaseHTTPRequestHandler):

    # --------------------------------------------------------
    # Disable excessive console logging
    # --------------------------------------------------------

    def log_message(self, format, *args):
        print("[SERVER]", format % args)

    # --------------------------------------------------------
    # Send response
    # --------------------------------------------------------

    def send_json(self, data, status=200):

        response = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(response))
        )

        self.end_headers()

        self.wfile.write(response)

    # --------------------------------------------------------
    # GET REQUESTS
    # --------------------------------------------------------

    def do_GET(self):

        parsed_path = urlparse(self.path)

        path = parsed_path.path

        # ----------------------------------------------------
        # Main page
        # ----------------------------------------------------

        if path == "/":
            self.serve_file(
                "index.html",
                "text/html; charset=utf-8"
            )
            return

        # ----------------------------------------------------
        # CSS
        # ----------------------------------------------------

        if path == "/style.css":
            self.serve_file(
                "style.css",
                "text/css; charset=utf-8"
            )
            return

        # ----------------------------------------------------
        # JavaScript
        # ----------------------------------------------------

        if path == "/script.js":
            self.serve_file(
                "script.js",
                "application/javascript; charset=utf-8"
            )
            return

        # ----------------------------------------------------
        # Health check
        # ----------------------------------------------------

        if path == "/api/health":

            self.send_json(
                {
                    "status": "ok",
                    "message": "History Teaching Agent is running."
                }
            )

            return

        # ----------------------------------------------------
        # Not found
        # ----------------------------------------------------

        self.send_json(
            {
                "error": "Page not found."
            },
            404
        )

    # --------------------------------------------------------
    # POST REQUESTS
    # --------------------------------------------------------

    def do_POST(self):

        parsed_path = urlparse(self.path)

        if parsed_path.path != "/api/chat":

            self.send_json(
                {
                    "error": "Invalid API endpoint."
                },
                404
            )

            return

        try:

            # ------------------------------------------------
            # Read request body
            # ------------------------------------------------

            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            body = self.rfile.read(content_length)

            data = json.loads(
                body.decode("utf-8")
            )

            student_question = data.get(
                "question",
                ""
            ).strip()

            # ------------------------------------------------
            # Validate question
            # ------------------------------------------------

            if not student_question:

                self.send_json(
                    {
                        "error": "Please enter a question."
                    },
                    400
                )

                return

            # ------------------------------------------------
            # Prevent extremely large requests
            # ------------------------------------------------

            if len(student_question) > 3000:

                self.send_json(
                    {
                        "error": "Question is too long. Please keep it under 3000 characters."
                    },
                    400
                )

                return

            print(
                "\nStudent:",
                student_question
            )

            # ------------------------------------------------
            # Ask Hugging Face
            # ------------------------------------------------

            answer = ask_ai(
                student_question
            )

            print(
                "AI:",
                answer
            )

            # ------------------------------------------------
            # Return answer
            # ------------------------------------------------

            self.send_json(
                {
                    "answer": answer
                }
            )

        except json.JSONDecodeError:

            self.send_json(
                {
                    "error": "Invalid JSON request."
                },
                400
            )

        except Exception as error:

            print(
                "ERROR:",
                repr(error)
            )

            self.send_json(
                {
                    "error": (
                        "The AI service could not process the request. "
                        "Please check the terminal for details."
                    )
                },
                500
            )

    # --------------------------------------------------------
    # SERVE FRONTEND FILES
    # --------------------------------------------------------

    def serve_file(
        self,
        filename,
        content_type
    ):

        file_path = os.path.join(
            FRONTEND_FOLDER,
            filename
        )

        if not os.path.exists(file_path):

            self.send_json(
                {
                    "error": "Frontend file not found: " + filename
                },
                404
            )

            return

        try:

            with open(
                file_path,
                "rb"
            ) as file:

                content = file.read()

            self.send_response(200)

            self.send_header(
                "Content-Type",
                content_type
            )

            self.send_header(
                "Content-Length",
                str(len(content))
            )

            self.end_headers()

            self.wfile.write(content)

        except Exception as error:

            print(
                "File error:",
                repr(error)
            )

            self.send_json(
                {
                    "error": "Could not load frontend file."
                },
                500
            )


# ============================================================
# START SERVER
# ============================================================

def start_server():

    # Render provides PORT automatically.
    # Locally, use port 8000.
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8000))

    server = HTTPServer(
        (host, port),
        TeachingAgentHandler
    )

    print("=" * 60)
    print("CLASS 10 HISTORY AI TEACHING ASSISTANT")
    print("=" * 60)
    print()
    print("Server is running on port:")
    print(port)
    print()
    print("For local browser access, open:")
    print("http://127.0.0.1:{}".format(port))
    print()
    print("or:")
    print("http://localhost:{}".format(port))
    print()
    print("Press CTRL+C to stop the server.")
    print("=" * 60)

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nServer stopped.")

    finally:
        server.server_close()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    start_server()