document.addEventListener('DOMContentLoaded', () => {

    const chatbot2Entity = document.getElementById('chatbot2-container');
    const closeChatButton = document.getElementById('closeChatbot');

    const hideChatbotContainer = () => {
        if (chatbot2Entity) {
            chatbot2Entity.style.display = 'none';
        }
    };

    const handleCloseButton = () => {
        if (closeChatButton) {
            hideChatbotContainer();
        }
    };

    const addCloseButtonListener = () => {
        if (closeChatButton) {
            closeChatButton.addEventListener('click', handleCloseButton);
        }
    };

    const renderChatbot = () => {
        if (chatbot2Entity && closeChatButton) {
            addCloseButtonListener(); 
        }
    };

    renderChatbot();
});
