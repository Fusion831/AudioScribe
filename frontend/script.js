document.addEventListener('DOMContentLoaded', () => {
    
    const imageUpload = document.getElementById('imageUpload');
    const statusText = document.getElementById('statusText');
    const loader = document.getElementById('loader');
    const interactiveArea = document.getElementById('interactive-area');

    
    let lastDescription = '';

    
    const BACKEND_URL = 'http://127.0.0.1:8000/api/describe-image';

    
    imageUpload.addEventListener('change', handleImageUpload);

    
    async function handleImageUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

       
        updateStatus('Image uploaded. Analyzing, please wait...', true);
        interactiveArea.innerHTML = ''; // Clear old buttons

        const formData = new FormData();
        formData.append('file', file);

        try {
            // --- API Call to Backend ---
            const response = await fetch(BACKEND_URL, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                // Try to get a more specific error from the backend
                const errorData = await response.json().catch(() => ({ detail: 'An unknown server error occurred.' }));
                throw new Error(errorData.detail || `HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            const description = data.description;
            
            if (description) {
                lastDescription = description;
                updateStatus('Analysis complete. Playing audio...', false);
                speakText(description, () => {
                    // This callback runs after the speech is finished
                    updateStatus('Ready for a new photo or follow-up action.');
                    createInteractiveButtons();
                });
            } else {
                throw new Error('Received an empty description from the server.');
            }

        } catch (error) {
            console.error('Error during analysis:', error);
            const errorMessage = `Analysis failed: ${error.message}`;
            updateStatus(errorMessage, false);
            speakText(errorMessage);
        }
    }

    
    function speakText(text, onEndCallback) {
        // Cancel any currently speaking utterance
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        
        
        if (onEndCallback) {
            utterance.onend = onEndCallback;
        }

        window.speechSynthesis.speak(utterance);
    }

    
    function updateStatus(message, isLoading) {
        statusText.textContent = message;
        loader.hidden = !isLoading;
    }

    
    function createInteractiveButtons() {
        interactiveArea.innerHTML = ''; // Clear previous buttons

        const readAgainButton = document.createElement('button');
        readAgainButton.textContent = 'Read That Again';
        readAgainButton.onclick = () => {
            if (lastDescription) {
                // Re-speak the last description and provide feedback
                updateStatus('Repeating the last description...', false);
                speakText(lastDescription, () => {
                    updateStatus('Ready for a new photo or follow-up action.');
                });
            }
        };

        interactiveArea.appendChild(readAgainButton);
    }
});