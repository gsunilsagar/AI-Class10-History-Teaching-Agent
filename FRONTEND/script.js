// ============================================================
// CLASS 10 HISTORY AI TEACHING ASSISTANT
// ============================================================


// ============================================================
// GET HTML ELEMENTS
// ============================================================

const chatMessages =
    document.getElementById("chatMessages");

const questionInput =
    document.getElementById("questionInput");

const sendButton =
    document.getElementById("sendButton");

const loading =
    document.getElementById("loading");


// ============================================================
// ADD MESSAGE TO CHAT
// ============================================================

function addMessage(
    sender,
    text
) {

    const message =
        document.createElement("div");

    message.classList.add(
        "message"
    );


    // --------------------------------------------------------
    // USER MESSAGE
    // --------------------------------------------------------

    if (sender === "user") {

        message.classList.add(
            "user-message"
        );

        message.innerHTML = `
            <div class="avatar">
                You
            </div>

            <div class="message-content">

                <div class="message-name">
                    Student
                </div>

                <div class="message-text">
                    ${escapeHTML(text)}
                </div>

            </div>
        `;
    }


    // --------------------------------------------------------
    // AI MESSAGE
    // --------------------------------------------------------

    else {

        message.classList.add(
            "ai-message"
        );

        message.innerHTML = `
            <div class="avatar">
                AI
            </div>

            <div class="message-content">

                <div class="message-name">
                    History Teacher
                </div>

                <div class="message-text">
                    ${formatAIResponse(text)}
                </div>

            </div>
        `;
    }


    chatMessages.appendChild(
        message
    );


    // Automatically scroll to newest message

    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// ============================================================
// ESCAPE HTML
// ============================================================

function escapeHTML(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// ============================================================
// FORMAT AI RESPONSE
// ============================================================

function formatAIResponse(text) {

    let safeText =
        escapeHTML(text);


    // Convert line breaks

    safeText =
        safeText.replace(
            /\r\n/g,
            "\n"
        );


    safeText =
        safeText.replace(
            /\n\n+/g,
            "</p><p>"
        );


    safeText =
        safeText.replace(
            /\n/g,
            "<br>"
        );


    return "<p>" +
        safeText +
        "</p>";
}


// ============================================================
// SHOW LOADING
// ============================================================

function showLoading() {

    loading.classList.remove(
        "hidden"
    );

    sendButton.disabled = true;

    questionInput.disabled = true;
}


// ============================================================
// HIDE LOADING
// ============================================================

function hideLoading() {

    loading.classList.add(
        "hidden"
    );

    sendButton.disabled = false;

    questionInput.disabled = false;

    questionInput.focus();
}


// ============================================================
// SEND QUESTION TO BACKEND
// ============================================================

async function sendQuestion() {

    const question =
        questionInput.value.trim();


    // --------------------------------------------------------
    // Empty question
    // --------------------------------------------------------

    if (!question) {

        questionInput.focus();

        return;
    }


    // --------------------------------------------------------
    // Show student's question
    // --------------------------------------------------------

    addMessage(
        "user",
        question
    );


    // Clear input

    questionInput.value = "";


    // Show loading

    showLoading();


    try {

        // ----------------------------------------------------
        // Send request to Python backend
        // ----------------------------------------------------

        const response =
            await fetch(
                "/api/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );


        // ----------------------------------------------------
        // Convert response to JSON
        // ----------------------------------------------------

        const data =
            await response.json();


        // ----------------------------------------------------
        // Check for errors
        // ----------------------------------------------------

        if (!response.ok) {

            throw new Error(
                data.error ||
                "The server returned an error."
            );
        }


        // ----------------------------------------------------
        // Display AI answer
        // ----------------------------------------------------

        addMessage(
            "ai",
            data.answer
        );


    } catch (error) {

        console.error(
            "Error:",
            error
        );


        addMessage(
            "ai",
            "Sorry, I could not process your question right now. Please check that the Python server is running and try again."
        );

    } finally {

        hideLoading();
    }
}


// ============================================================
// SEND BUTTON
// ============================================================

sendButton.addEventListener(
    "click",
    sendQuestion
);


// ============================================================
// ENTER KEY
// ============================================================

questionInput.addEventListener(
    "keydown",
    function(event) {

        // Enter = send

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendQuestion();
        }

    }
);


// ============================================================
// INITIAL FOCUS
// ============================================================

questionInput.focus();