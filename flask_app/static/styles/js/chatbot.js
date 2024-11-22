document.getElementById('sendBtn').addEventListener('click', function() {
    var userInput = document.getElementById('userInput').value;
    console.log("User input:", userInput);  // Log user input for testing

    if (userInput.trim() !== "") {
        addChat(userInput, 'user');
        getBotResponse(userInput);
        document.getElementById('userInput').value = '';
    }
});

function addChat(message, sender) {
    const chatbox = document.getElementById('chatbox');
    let messageDiv = document.createElement('div');
    messageDiv.textContent = sender + ': ' + message;
    chatbox.appendChild(messageDiv);
    chatbox.scrollTop = chatbox.scrollHeight; // Scroll to the bottom
}

function getBotResponse(message) {
    console.log("Sending message to chatbot API:", message);  // Log outgoing message

    fetch('/chatbot-api', {  // Calls the Flask API route
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => {
        console.log("Response Status:", response.status);  // Log response status

        if (!response.ok) { // Check if the response is OK
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log("Full Response Data:", data);  // Log full response data

        const reply = data.reply || 'No response'; // Safely access the reply
        console.log("Bot reply:", reply);  // Log bot reply for debugging
        addChat(reply, 'bot');
    })
    .catch(error => {
        console.error('Error:', error);
        addChat('Error retrieving response', 'bot'); // Display an error message in the chat
    });
}