document.addEventListener("DOMContentLoaded", function() {
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    const chatHistory = document.querySelector(".chat-history");

    sendButton.addEventListener("click", function() {
        const messageText = messageInput.value;

        if (messageText.trim() !== "") {
            const messageElement = document.createElement("div");
            messageElement.classList.add("message");
            messageElement.textContent = messageText;

            chatHistory.appendChild(messageElement);
            messageInput.value = "";

            // Прокрутите историю чата вниз, чтобы видеть новые сообщения
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
    });
});