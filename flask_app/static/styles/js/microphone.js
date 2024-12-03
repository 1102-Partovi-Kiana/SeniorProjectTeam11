document.getElementById('mic-button').addEventListener('click', () => {
    startSpeechRecognition();
});

function startSpeechRecognition() {
    const searchField = getSearchField();
    const searchButton = getSearchButton();
    const speechAPI = getSpeechAPI();

    if (!speechAPI) {
        showAlert();
        return;
    }

    const recognizer = createRecognition(speechAPI);
    setupRecognitionEvents(recognizer, searchField, searchButton);
    startRecognition(recognizer);
}

function getSearchField() {
    return document.getElementById('search-input');
}

function getSearchButton() {
    return document.getElementById('search-button');
}

function getSpeechAPI() {
    return window.webkitSpeechRecognition;
}

function showAlert() {
    alert('Speech recognition not supported in this browser.');
}

function createRecognition(speechAPI) {
    const recognition = new speechAPI();
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;
    return recognition;
}

function setupRecognitionEvents(recognizer, inputField, searchButton) {
    recognizer.onstart = () => {
        logMessage('Voice recognition started. Speak into the microphone.');
    };

    recognizer.onresult = (event) => {
        handleRecognitionResult(event, inputField);
    };

    recognizer.onend = () => {
        handleRecognitionEnd(searchButton);
    };

    recognizer.onerror = (event) => {
        handleRecognitionError(event);
    };
}

function handleRecognitionResult(event, inputField) {
    const transcript = processTranscript(event.results[0][0].transcript);
    setInputFieldValue(inputField, transcript);
    logMessage('Transcript: ' + transcript);
}

function processTranscript(transcript) {
    return transcript.replace(/\.$/, '');
}

function setInputFieldValue(inputField, value) {
    inputField.value = value;
}

function handleRecognitionEnd(searchButton) {
    logMessage('Voice recognition ended.');
    triggerSearch(searchButton);
}

function triggerSearch(searchButton) {
    searchButton.click();
}

function handleRecognitionError(event) {
    logError('Error in recognition: ' + event.error);
    alert('An error occurred while using voice recognition. Please try again.');
}

function startRecognition(recognition) {
    recognition.start();
}

function logMessage(message) {
    console.log(message);
}

function logError(error) {
    console.error(error);
}

document.getElementById('search-button').addEventListener('click', () => {
    getSearch();
});

function getSearch() {
    const query = getSearchQuery();
    logMessage('Searching for: ' + query);
}

function getSearchQuery() {
    const inputField = getSearchField();
    return inputField.value;
}


