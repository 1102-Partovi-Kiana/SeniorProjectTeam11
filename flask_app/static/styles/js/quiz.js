$(document).ready(function () {
    
    let state = {
        questions_served: 0,
        score: 0,
        difficulty: 'easy',
        used_questions: [],
        last_correct: true  
    };

    function startQuiz() {
        state = {
            questions_served: 0,
            score: 0,
            difficulty: 'easy',
            used_questions: [],
            last_correct: true
        };
        fetchNextQuestion(); // Get the next question
    }

    function fetchNextQuestion() { // use the POST call
        $.ajax({
            url: `/next-question/${quiz_id}`,
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(state),
            success: function (response) {
                if (response.done) {
                    displayResult(response.score, response.message);
                    return;
                }

                // Quiz adaptation features where quiz content is updated
                state.questions_served = response.questions_served;
                state.score = response.score;
                state.difficulty = response.difficulty;
                state.used_questions = response.used_questions;
                state.last_correct = true;  

                //Displays the progress text
                $("#progress").html(`Question ${response.questions_served} out of ${response.total_questions}`);

                const question = response.question;

                renderQuestion(question);
            },
            error: function (error) {
                console.error("Error fetching question:", error);
                alert("An error occurred while fetching the question. Please try again.");
            }
        });
    }

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

    function displayResult(score) {
        $("#quiz-container").html(`
            <div class="result text-center">
                <h3 class="mb-3">Quiz Complete!</h3>
                <p>Thank you for taking the quiz.</p>
                <p>Your score: ${score}/10</p>
                <div id="score-summary" class="mt-3"></div>
                <button id="restart-btn" class="btn btn-success mt-3">Restart Quiz</button>
            </div>
        `);
    
        $("#progress").html("");
    
        const subsectionNumber = $("#quiz-container").data("subsection");

        // Send score to backend
        $.ajax({
            url: `/get-scores?subsection_number=${subsectionNumber}`,
            method: "GET",
            success: function(response) {
                console.log("Scores:", response);
            },
            error: function(error) {
                console.error("Error fetching scores:", error);
            }
        });

        $.ajax({
            url: "/submit-quiz",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                score: score,
                total_questions: 10,
                subsection_number: subsectionNumber
            }),
            success: function (response) {
                console.log("Quiz results saved:", response);
    
                let scoreSummary = `
                    <p>Most Recent Score: ${response.most_recent_score}%</p>
                    <p>Highest Score: ${response.highest_score}%</p>
                    <p>Passing Score: ${response.passing_score}%</p>
                `;
                $("#score-summary").html(scoreSummary);
    
                if (response.most_recent_score >= response.passing_score || response.highest_score >= response.passing_score) {
                    $("#next-section").show();
                }
            },
            error: function (error) {
                console.error("Error saving quiz results:", error);
                alert("Error saving quiz results. Please try again.");
            }
        });
    
        $("#restart-btn").click(function () {
            startQuiz();
        });
    }
    

    function renderStartScreen() {
        const subsectionNumber = $("#quiz-container").data("subsection");
        fetch(`/get-scores?subsection_number=${subsectionNumber}`)
            .then(response => response.json())
            .then(data => {
                const hasPassingScore = (data.recent_score >= data.passing_score) || (data.highest_score >= data.passing_score);
    
                $("#quiz-container").html(`
                    <h2 class="text-center">Press Start to begin the quiz.</h2>
                    <div class="text-center">
                        <p>Most Recent Score: ${data.recent_score ? `${data.recent_score}%` : 'N/A'}</p>
                        <p>Highest Score: ${data.highest_score ? `${data.highest_score}%` : 'N/A'}</p>
                        <p>Passing Score: ${data.passing_score ? `${data.passing_score}%` : 'N/A'}</p>
                        <button id="start-button" class="btn btn-primary">Start Quiz</button>
                    </div>
                `);
    
                $("#progress").html("");

                if (hasPassingScore) {
                    $("#next-section").show();
                }
    
                $("#start-button").click(function () {
                    $(this).hide();
                    fetchNextQuestion();
                });
            })
            .catch(error => {
                console.error('Error fetching scores:', error);
                $("#quiz-container").html(`<p class="text-center text-danger">Failed to load scores. Please try again.</p>`);
            });
    }
    
    
    renderStartScreen();
});
