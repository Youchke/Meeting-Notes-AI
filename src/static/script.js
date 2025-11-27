const fileInput = document.getElementById('file-input');
const uploadSection = document.getElementById('upload-section');
const statusSection = document.getElementById('status-section');
const resultSection = document.getElementById('result-section');
const statusText = document.getElementById('status-text');

fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    uploadSection.classList.add('hidden');
    statusSection.classList.remove('hidden');

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        pollStatus(data.task_id);
    } catch (error) {
        console.error('Error:', error);
        alert('Upload failed');
        reset();
    }
});

async function pollStatus(taskId) {
    const interval = setInterval(async () => {
        try {
            const response = await fetch(`/api/status/${taskId}`);
            const data = await response.json();
            console.log("Poll status:", data);

            if (data.status === 'Completed') {
                clearInterval(interval);
                console.log("Task completed, showing results:", data.result);
                showResults(data.result);
            } else if (data.status === 'Failed') {
                clearInterval(interval);
                alert(`Processing failed: ${data.error}`);
                reset();
            } else {
                statusText.textContent = `Processing... (${data.status})`;
            }
        } catch (error) {
            clearInterval(interval);
            console.error('Polling error:', error);
        }
    }, 2000);
}

function showResults(result) {
    statusSection.classList.add('hidden');
    resultSection.classList.remove('hidden');

    document.getElementById('summary-content').textContent = result.meeting_summary;
    document.getElementById('transcription-content').textContent = result.transcription;
}

function openTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));

    document.getElementById(tabName).classList.add('active');
    // Find the button that corresponds to this tab. 
    // Since the button calls this function, we can use event.currentTarget if available, 
    // but openTab might be called programmatically.
    // A safer way for the tab buttons:
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => {
        if (btn.textContent.includes(tabName === 'summary' ? 'Summary' : 'Transcription')) {
            btn.classList.add('active');
        }
    });
}

async function copyToClipboard(elementId) {
    const text = document.getElementById(elementId).textContent;
    try {
        await navigator.clipboard.writeText(text);
        alert('Text copied to clipboard!');
    } catch (err) {
        console.error('Failed to copy text: ', err);
        alert('Failed to copy text.');
    }
}

function reset() {
    fileInput.value = '';
    resultSection.classList.add('hidden');
    statusSection.classList.add('hidden');
    uploadSection.classList.remove('hidden');
}
