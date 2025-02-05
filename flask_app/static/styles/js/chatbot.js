document.addEventListener('DOMContentLoaded', () => {
    const hintsButton = document.getElementById('hints-button');
    const hintBoxContainer = document.getElementById('hintbox-container');
    const hintBox = document.getElementById('hintbox');
    const addtab = document.getElementById('popup-window-additional-tab');

    const maxHints = 4; 

    let globalHintCount = 0;
    if (!sessionStorage.getItem('globalHintCount')) {
        sessionStorage.setItem('globalHintCount', '0');
        globalHintCount = 0;
        console.log('globalHintCount = 0.');
    } else {
        globalHintCount = parseInt(sessionStorage.getItem('globalHintCount'), 10);
        console.log(`Existing globalHintCount: ${globalHintCount}`);
        if (globalHintCount >= maxHints) {
            lockHintsButton();
        }
    }

    function lockHintsButton() {
        hintsButton.disabled = true;
        hintsButton.style.cursor = 'not-allowed';
        hintsButton.title = 'No more hints available.';
        hintBox.innerHTML = '<li>No additional hints are available.</li>';
        addtab.innerHTML = '<p>No additional hints are available.</p>';
        hintBoxContainer.style.display = 'block';
    }

    function getHintsButton() {
        hintsButton.disabled = false;
        hintsButton.style.cursor = 'pointer';
        hintsButton.title = 'Click to get a hint.';
    }

    function displayHints(hintsToAdd) {
        hintsToAdd.forEach((hint, index) => {
            const hintNumber = globalHintCount - hintsToAdd.length + index + 1;
            const hintItem = document.createElement('li');
            hintItem.textContent = `${hintNumber}. ${hint}`;
            hintBox.appendChild(hintItem);
            console.log(`Displayed Hint ${hintNumber}: ${hint}`);
        });

        if (hintsToAdd.length > 0) {
            addtab.innerHTML = `<p>Hint ${globalHintCount}: ${hintsToAdd[hintsToAdd.length - 1]}</p>`;
        } else {
            addtab.innerHTML = '<p>No additional hints are available.</p>';
        }

        hintBoxContainer.style.display = 'block';
    }

    hintsButton.addEventListener('click', async () => {
        console.log('Hints button clicked.');

        if (hintsButton.disabled) {
            return;
        }

        if (globalHintCount >= maxHints) {
            console.log('Maximum number of hints reached.');
            lockHintsButton();
            return;
        }

        const code = codeEditor.getValue(); 
        const errorLine = getErrorLine();
        const errorMessage = getErrorMessage(); 
        const hintLevel = getHintLevel(); 

        console.log('Fetching hints with the following parameters:', {
            code,
            errorLine,
            errorMessage,
            hintLevel,
        });

        const hints = await fetchHints({
            code,
            errorLine,
            errorMessage,
            hintLevel,
        });

        console.log(`Hints fetched: ${hints.length}`, hints);

        const validHints = hints.filter(hint => typeof hint === 'string' && hint.trim() !== '');
        console.log(`Valid hints after filtering: ${validHints.length}`, validHints);

        if (validHints.length > 0) {
            const hint = validHints[0];
            globalHintCount += 1;
            sessionStorage.setItem('globalHintCount', globalHintCount.toString());
            console.log(`Updated globalHintCount: ${globalHintCount}`);

            const hintNumber = globalHintCount;
            const hintItem = document.createElement('li');
            hintItem.textContent = `${hintNumber}. ${hint}`;
            hintBox.appendChild(hintItem);
            addtab.innerHTML = `<p>Hint ${hintNumber}: ${hint}</p>`;
            hintBoxContainer.style.display = 'block';
            console.log(`Displayed Hint ${hintNumber}: ${hint}`);

            if (globalHintCount >= maxHints) {
                console.log('Maximum hints reached after this hint.');
                lockHintsButton();
            } else {
                geteHintsButton();
            }
        } else {
            console.log('No valid hints returned from fetch.');
            lockHintsButton();
        }
    });
});

async function fetchHints({ code, errorLine, errorMessage, hintLevel }) {
    console.log('Fetching hints from the server...');

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

    console.log("Including page_context in API request:", pageContext);

    try {
        const response = await fetch('/chatbot-api', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                code,
                error_line: errorLine,
                error_message: errorMessage,
                hint_level: hintLevel, 
                page_context: pageContext, 
            }),
        });

        console.log(`Fetch response status: ${response.status}`);

        if (!response.ok) {
            throw new Error(`Failed to fetch hints: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Hints received from server:', data.hints);
        return data.hints || [];
    } catch (error) {
        console.error('Error fetching hints:', error);
        return ['Error fetching hints. Please try again.'];
    }
}

