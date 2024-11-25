$(document).ready(function () {
    // Initialize the quiz state
    let state = {
        questions_served: 0,
        score: 0,
        difficulty: 'easy',
        used_questions: [],
        last_correct: true  // Initial assumption; can be set to null if preferred
    };

    // Function to start the quiz
    function startQuiz() {
        // Reset the state
        state = {
            questions_served: 0,
            score: 0,
            difficulty: 'easy',
            used_questions: [],
            last_correct: true
        };
        // Fetch the first question
        fetchNextQuestion();
    }

    // Function to fetch the next question from the server
    function fetchNextQuestion() {
        $.ajax({
            url: "/next-question",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(state),
            success: function (response) {
                if (response.done) {
                    displayResult(response.score, response.message);
                    return;
                }

                // Update the state based on server response
                state.questions_served = response.questions_served;
                state.score = response.score;
                state.difficulty = response.difficulty;
                state.used_questions = response.used_questions;
                state.last_correct = true;  // Reset for the next question

                const question = response.question;

                // Render the question
                renderQuestion(question);
            },
            error: function (error) {
                console.error("Error fetching question:", error);
                alert("An error occurred while fetching the question. Please try again.");
            }
        });
    }

    // Function to render a question on the page
    function renderQuestion(questionData) {
        const question = questionData.question;
        const options = questionData.options;
        const correctAnswerIndex = questionData.answer;

        $("#quiz-container").html(`
            <div class="question mb-4">
                <h5>${question}</h5>
                <div class="options">
                    ${options.map((option, index) => `
                        <div class="form-check">
                            <input type="radio" class="form-check-input" name="question" value="${index}" id="option${index}">
                            <label class="form-check-label" for="option${index}">${option}</label>
                        </div>
                    `).join("")}
                </div>
                <button id="submit-btn" class="btn btn-primary mt-3">Submit</button>
            </div>
        `);

        // Submit Button Handler
        $("#submit-btn").click(function () {
            const selected = $("input[name='question']:checked").val();
            if (selected !== undefined) {
                const selectedIndex = parseInt(selected);
                const isCorrect = selectedIndex === correctAnswerIndex;
                if (isCorrect) {
                    state.score += 1;
                }
                state.last_correct = isCorrect;
                fetchNextQuestion();
            } else {
                alert("Please select an answer!");
            }
        });
    }

    // Function to display the quiz results
    function displayResult(score, message) {
        $("#quiz-container").html(`
            <div class="result text-center">
                <h3 class="mb-3">Quiz Complete!</h3>
                <p>Thank you for taking the quiz.</p>
                <p>Your score: ${score}/10</p>
                <button id="restart-btn" class="btn btn-success mt-3">Restart Quiz</button>
            </div>
        `);

        // Restart Quiz Button Handler
        $("#restart-btn").click(function () {
            startQuiz();
        });
    }

    // Function to render the initial start screen
    function renderStartScreen() {
        $("#quiz-container").html(`
            <h2 class="text-center">Press Start to begin the quiz.</h2>
            <div class="text-center">
                <button id="start-button" class="btn btn-primary">Start Quiz</button>
            </div>
        `);

        // Start Button Handler
        $("#start-button").click(function () {
            $(this).hide();
            fetchNextQuestion();
        });
    }

    // Initialize the quiz by rendering the start screen
    renderStartScreen();
});
