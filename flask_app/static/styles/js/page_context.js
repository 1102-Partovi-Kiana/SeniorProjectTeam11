const pageContexts = {
    "/Fetch-Reach-Robot": "Fetch Reach",
    "/PickAndPlacePage": "Fetch Pick and Place",
    "/FetchStackPage": "Fetch Stack",
    "/FetchOrganizePage": "Fetch Organize",
    "/FetchOrganizeSensorsPage": "Fetch Sensors",
    "/CarPage": "Car",
};

const currentPath = window.location.pathname;
const pageContext = pageContexts[currentPath] || "General";

console.log("Current Path:", currentPath);
console.log("Used page_context:", pageContext);

fetch('/chatbot-api', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        page_context: pageContext,  
        code: codeEditor.getValue(),  
        error_line: getErrorLine(),  
        error_message: getErrorMessage(),  
    }),
})
.then(response => response.json())
.then(data => console.log('Response from API:', data))  
.catch(error => console.error('Error:', error));


async function runUserCode() {
    const code = codeEditor.getValue();

    const pageContexts = {
        "/Fetch-Reach-Robot": "Fetch Reach",
        "/PickAndPlacePage": "Fetch Pick and Place",
        "/FetchStackPage": "Fetch Stack",
        "/FetchOrganizePage": "Fetch Organize",
        "/FetchOrganizeSensorsPage": "Fetch Sensors",
        "/CarPage": "Car",
    };

    const currentPath = window.location.pathname;
    const pageContext = pageContexts[currentPath] || "General"; 

    console.log("Current Path:", currentPath);
    console.log("Used Page Context:", pageContext);

    const requestBody = JSON.stringify({
        code,
        context: pageContext, 
    });

    console.log("JSON Sent to Backend:", requestBody);  

    try {
        const response = await fetch('/run-code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }, 
            body: requestBody,  
        });

        console.log(`Fetch response status: ${response.status}`);

        if (!response.ok) {
            throw new Error(`Failed to run code: ${response.statusText}`);
        }

        const data = await response.json();
    } catch (error) {
        console.error("Uh Oh, Error running code:", error);
    }
}
