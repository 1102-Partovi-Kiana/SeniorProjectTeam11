document.addEventListener('DOMContentLoaded', function () {
    const sendBtn2 = document.getElementById('sendBtn2');
    const userInput2 = document.getElementById('userInput2');
    const chatbox2 = document.getElementById('chatbox2');
    const chatbotButton = document.querySelector('.chatbot-button');
    const chatbotContainer = document.getElementById('chatbot2-container');
    const chatbotLabel = document.querySelector('.chatbot-label'); 

    // Pages for more personalized experience
    const pageContexts = {
        '/': 'Homepage',
        '/signup': 'Sign Up',
        '/login': 'Log In',
        '/courses': 'Courses',
    };

    const currentPath = window.location.pathname;
    const pageContext = pageContexts[currentPath] || 'General'; 

    setTimeout(() => {
        if (chatbotLabel) {
            chatbotLabel.style.opacity = '0'; 
            chatbotLabel.style.transition = 'opacity 1s ease'; 

            setTimeout(() => {
                chatbotLabel.style.display = 'none'; 
                chatbotButton.style.marginBottom = '0px';
            }, 1000);
        }
    }, 2000); 

    chatbotButton.addEventListener('click', function () {
        if (chatbotContainer.style.display === 'none' || chatbotContainer.style.display === '') {
            chatbotContainer.style.display = 'block';
        } else {
            chatbotContainer.style.display = 'none';
        }
    });

    function sendMessage2() {
        const userMessage = userInput2.value.trim();
        if (!userMessage) return;

        addChat(userMessage, 'user', chatbox2);
        userInput2.value = '';

        fetch('/chatbot-api-2', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: userMessage,
                page_context: pageContext 
            })
        })
            .then(response => response.json())
            .then(data => {
                const botReply = data.reply || 'Sorry, I didn’t understand that.';
                addChat(botReply, 'bot', chatbox2);
                chatbox2.scrollTop = chatbox2.scrollHeight;
            })
            .catch(() => {
                addChat('An error occurred. Please try again later.', 'bot', chatbox2);
            });
    }

    sendBtn2.addEventListener('click', sendMessage2);
    userInput2.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') sendMessage2();
    });

    function addChat(message, sender, chatbox) {
        const messageDiv = document.createElement('div');
        messageDiv.className = sender === 'user' ? 'user-message' : 'bot-reply';
        messageDiv.textContent = message;
        chatbox.appendChild(messageDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
    }
});
