document.addEventListener('DOMContentLoaded', () => {
    const hintsButton = document.getElementById('hints-button');
    const dropdownMenu = document.getElementById('hints-dropdown');
    const hintBoxContainer = document.getElementById('hintbox-container');
    const hintBox = document.getElementById('hintbox');

    const pageContexts = {
        '/Fetch-Reach-Robot': 'Fetch Reach',
        '/PickAndPlacePage': 'Fetch Pick and Place',
    };

    const currentPath = window.location.pathname;
    const pageContext = pageContexts[currentPath] || 'General';

    let hints = [];

    hintsButton.addEventListener('mouseenter', async () => {
        const code = ""; 

        try {
            const response = await fetch('/chatbot-api', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code, page_context: pageContext })
            });

            if (!response.ok) {
                throw new Error('Failed to fetch hints');
            }

            const data = await response.json();
            hints = data.hints || [];
            populateDropdownMenu(hints);
        } catch (error) {
            console.error('Error fetching hints:', error);
            hints = [];
            populateDropdownMenu([]);
        }
    });

    function populateDropdownMenu(hints) {
        dropdownMenu.innerHTML = ''; 
        const closeButton = document.createElement('button');
        closeButton.className = 'dropdown-close';
        closeButton.textContent = 'X';
        closeButton.style.cssText = 'float: right; background: none; border: none; font-size: 18px; cursor: pointer; padding: 5px; color: red;';
        closeButton.addEventListener('click', () => {
            dropdownMenu.style.display = 'none';
            hintBoxContainer.style.display = 'none'; 
        });
    
        dropdownMenu.appendChild(closeButton);
    
        if (hints.length > 0) {
            hints.forEach((hint, index) => {
                const listItem = document.createElement('li');
                const button = document.createElement('button');
                button.className = 'dropdown-item';
                button.dataset.hint = index + 1;
                button.textContent = `Get Hint ${index + 1}`;
                listItem.appendChild(button);
                dropdownMenu.appendChild(listItem);
            });
        } else {
            const noHintsItem = document.createElement('li');
            noHintsItem.textContent = 'No hints available';
            dropdownMenu.appendChild(noHintsItem);
        }
    
        dropdownMenu.style.display = 'block'; 
    }    

    dropdownMenu.addEventListener('click', (event) => {
        if (event.target.classList.contains('dropdown-item')) {
            const hintIndex = parseInt(event.target.dataset.hint, 10) - 1;
            if (hints[hintIndex]) {
                hintBox.innerHTML = `<li>${hints[hintIndex]}</li>`;
                hintBoxContainer.style.display = 'block'; 
            }
        }
    });

    window.addEventListener('load', () => {
        hintsButton.style.display = 'none'; 
        hintBoxContainer.style.display = 'none'; 
    });

    function updateHintBox(hints) {
        hintBox.innerHTML = ''; 

        if (hints && hints.length > 0) {
            hints.forEach((hint, index) => {
                const hintItem = document.createElement('li');
                hintItem.textContent = `${index + 1}. ${hint}`;
                hintBox.appendChild(hintItem);
            });
            hintBoxContainer.style.display = 'block'; 
        } else {
            const noHints = document.createElement('li');
            noHints.textContent = "No hints available.";
            hintBox.appendChild(noHints);
            hintBoxContainer.style.display = 'none'; 
        }
    }

    function getBotResponse(code, error) {
        fetch('/chatbot-api', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                code: code, 
                error: error, 
                page_context: pageContext 
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            hints = data.hints || [];
            updateHintBox(hints);

            if (hints.length > 0) {
                hintsButton.style.display = 'inline-block';
            } else {
                hintsButton.style.display = 'none'; 
            }
        })
        .catch(error => {
            console.error('Error:', error);
            updateHintBox([]); 
            hintsButton.style.display = 'none'; 
        });
    }
});
