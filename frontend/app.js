document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('chat-form');
    const input = document.getElementById('user-input');
    const chatHistory = document.getElementById('chat-history');
    const sendButton = document.getElementById('send-button');

    // Configure marked to sanitize and format markdown
    marked.setOptions({
        breaks: true,
        gfm: true
    });

    const checkIcon = `
        <svg class="step-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
    `;

    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function addUserMessage(text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message user-message';
        msgDiv.innerHTML = `
            <div class="message-content">
                ${escapeHTML(text)}
            </div>
        `;
        chatHistory.appendChild(msgDiv);
        scrollToBottom();
    }

    function createSystemMessageContainer() {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message system-message';

        // Structure: Steps container on top, Result container below
        msgDiv.innerHTML = `
            <div class="message-content">
                <div class="step-container" style="display: none;"></div>
                <div class="result-container markdown-body"></div>
            </div>
        `;

        chatHistory.appendChild(msgDiv);
        scrollToBottom();

        return {
            msgDiv,
            stepsEl: msgDiv.querySelector('.step-container'),
            resultEl: msgDiv.querySelector('.result-container')
        };
    }

    async function handleSubmission(e) {
        e.preventDefault();

        const query = input.value.trim();
        if (!query) return;

        // UI State: Loading
        input.value = '';
        input.disabled = true;
        sendButton.disabled = true;

        addUserMessage(query);
        const { stepsEl, resultEl } = createSystemMessageContainer();

        // Track the current active step so we can mark it done when the next one arrives
        let currentStepItem = null;

        try {
            const response = await fetch('/ai/stream', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });

            if (!response.ok) {
                throw new Error(`Server returned ${response.status}`);
            }

            // Fallback for reading streams in JS
            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let buffer = '';

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });

                // Parse Server-Sent Events (data: {...}\n\n)
                const parts = buffer.split('\n\n');
                buffer = parts.pop(); // Keep the last incomplete part in the buffer

                for (const part of parts) {
                    if (part.startsWith('data: ')) {
                        try {
                            const jsonStr = part.replace(/^data: /, '');
                            const payload = JSON.parse(jsonStr);

                            if (payload.type === 'step') {
                                stepsEl.style.display = 'flex';

                                // Mark previous step as "done" (green check)
                                if (currentStepItem) {
                                    currentStepItem.classList.remove('active');
                                    currentStepItem.querySelector('.step-spinner').outerHTML = checkIcon;
                                }

                                // Create new active step (spinner)
                                const stepDiv = document.createElement('div');
                                stepDiv.className = 'step-item active';
                                stepDiv.innerHTML = `
                                    <div class="step-spinner"></div>
                                    <span>${escapeHTML(payload.message)}</span>
                                `;
                                stepsEl.appendChild(stepDiv);
                                currentStepItem = stepDiv;
                                scrollToBottom();
                            }
                            else if (payload.type === 'result') {
                                // Mark the very final step as done
                                if (currentStepItem) {
                                    currentStepItem.classList.remove('active');
                                    currentStepItem.querySelector('.step-spinner').outerHTML = checkIcon;
                                }

                                // Render Markdown
                                resultEl.innerHTML = marked.parse(payload.message);
                                scrollToBottom();
                            }
                            else if (payload.type === 'error') {
                                resultEl.innerHTML = `<span class="error-text">Engine Error: ${escapeHTML(payload.message)}</span>`;
                                scrollToBottom();
                            }
                        } catch (err) {
                            console.error("Failed to parse SSE payload JSON", err);
                        }
                    }
                }
            }
        } catch (error) {
            console.error("Fetch stream error:", error);
            resultEl.innerHTML = `<span class="error-text">Network Error: Could not reach PulseMarine Engine.</span>`;
        } finally {
            // Restore UI Input state
            input.disabled = false;
            sendButton.disabled = false;
            input.focus();
            scrollToBottom();
        }
    }

    form.addEventListener('submit', handleSubmission);

    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g,
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag] || tag)
        );
    }
});
