const apiKey = "AIzaSyAfoQ856qhys1OONDyPMRR7LoArpKz2JSY";
const apiUrl = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent";

let popup = document.createElement("div");
popup.id = "explanation-popup";
document.body.appendChild(popup);

let lastMouseEvent = null; 
let allowNewExplanations = true; 
let currentRequestController = null; 

let isExplainerActive = false; 

document.getElementById("toggle-explainer").addEventListener("change", function () {
    isExplainerActive = this.checked;
    console.log("Explainer Active:", isExplainerActive);
});

document.addEventListener("mouseup", function (event) {
    if (!isExplainerActive) return; 

    if (event.target.id === "close-popup") {
        console.log("Close button clicked, ignoring event.");
        return; 
    }

    let selectedText = window.getSelection().toString().trim();
    let selectionParent = window.getSelection().anchorNode?.parentElement;

    if (!allowNewExplanations) return;

    if (selectedText.length > 0 && selectionParent && selectionParent.closest(".robotics-content")) {
        console.log("Text Selected:", selectedText);
        lastMouseEvent = event; 
        showExplanationPopup("Explaining...", lastMouseEvent); 
        fetchExplanation(selectedText, lastMouseEvent); 
    }
});

async function fetchExplanation(text, mouseEvent) {
    if (currentRequestController) {
        currentRequestController.abort();
    }

    currentRequestController = new AbortController(); 
    let signal = currentRequestController.signal;

    let requestBody = {
        contents: [{ parts: [{ text: `Explain this in simple terms with regards to simulated robotics: "${text}"` }] }]
    };

    console.log("Sending API Request:", requestBody);

    try {
        let response = await fetch(`${apiUrl}?key=${apiKey}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestBody),
            signal 
        });

        let data = await response.json();
        console.log("API Response:", data);

        if (data?.candidates?.length > 0) {
            let explanation = data.candidates[0].content.parts[0].text;
            console.log("Received Explanation:", explanation);
            showExplanationPopup(explanation, mouseEvent, false); 
        } else {
            console.error("No explanation found in API response.");
            showExplanationPopup("Error: No explanation received.", mouseEvent, false);
        }
    } catch (error) {
        if (error.name === "AbortError") {
            console.warn("Request aborted due to user action.");
        } else {
            console.error("API Request Failed:", error);
            showExplanationPopup("Error: Failed to fetch explanation.", mouseEvent, false);
        }
    }
}

function showExplanationPopup(text, mouseEvent, isLoading = true) {
    console.log("Displaying Explanation:", text);

    if (!mouseEvent) {
        console.warn("Mouse event is undefined, using default positioning.");
        mouseEvent = { pageX: window.innerWidth / 2, pageY: window.innerHeight / 2 }; 
    }

    popup.style.position = "absolute";
    popup.style.left = "auto";
    popup.style.top = "auto";
    popup.style.bottom = "auto";
    popup.style.right = "auto";
    popup.style.display = "block";

    const selection = window.getSelection();
    if (!selection.rangeCount) return;

    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect(); 

    let posX = rect.left + window.scrollX;
    let posY = rect.bottom + window.scrollY + 5;

    if (posX + popup.offsetWidth > window.innerWidth) {
        posX = window.innerWidth - popup.offsetWidth - 20; 
    }
    if (posY + popup.offsetHeight > window.innerHeight) {
        posY = window.innerHeight - popup.offsetHeight - 20;
    }

    popup.style.left = `${posX}px`;
    popup.style.top = `${posY}px`;

    let loadingIcon = isLoading ? `<span id="loading-icon"></span>` : "";

    popup.innerHTML = `
        <div id="explanation-header">
            <button id="close-popup">✕</button>
        </div>
        <div id="explanation-content">
            ${loadingIcon} <span id="explanation-text">${text}</span>
        </div>
        <div id="explanation-footer">
            Powered by Gemini AI
        </div>
    `;

    document.getElementById("close-popup").onclick = () => {
        popup.style.display = "none";
        allowNewExplanations = false; 

        if (currentRequestController) {
            currentRequestController.abort();
            currentRequestController = null;
        }

        setTimeout(() => {
            allowNewExplanations = true;
        }, 500);
    };
}
