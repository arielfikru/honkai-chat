document.addEventListener('DOMContentLoaded', function() {
    let conversation = JSON.parse(localStorage.getItem('conversation'));
    if (conversation) {
        document.getElementById('json-editor').value = JSON.stringify(conversation, null, 4);
    }

    document.getElementById('upload-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const fileInput = document.getElementById('file-input');
        const file = fileInput.files[0];
        
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const content = e.target.result;
                localStorage.setItem('conversation', content);
                document.getElementById('json-editor').value = content;
                alert('File uploaded and content loaded successfully');
            }
            reader.readAsText(file);
        } else {
            alert('No file selected');
        }
    });

    document.getElementById('save-json').addEventListener('click', function() {
        const jsonContent = document.getElementById('json-editor').value;

        try {
            const parsed = JSON.parse(jsonContent);
            localStorage.setItem('conversation', JSON.stringify(parsed, null, 4));
            showPopup('JSON saved successfully');
        } catch (e) {
            showPopup('Invalid JSON', 'error');
        }
    });

    function showPopup(message, type = 'success') {
        const popup = document.getElementById('popup');
        const popupMessage = document.getElementById('popup-message');
        const popupClose = document.getElementById('popup-close');

        popupMessage.textContent = message;
        popupMessage.classList.remove('text-green-500', 'text-red-500');
        popupMessage.classList.add(type === 'success' ? 'text-black-500' : 'text-red-500');
        popup.classList.remove('hidden');

        popupClose.addEventListener('click', function() {
            popup.classList.add('hidden');
        });
    }
});