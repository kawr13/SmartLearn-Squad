let username = JSON.parse(document.getElementById('user-name').textContent);
const chatID = JSON.parse(document.getElementById('chat-id').textContent);

const chatSocket = new ReconnectingWebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + chatID
    + '/'
);

function addMessageToChat(author, content, username) {
    const chatHistory = document.querySelector('#chat-history');
    let messageElement = document.createElement('div');
    let msgListTag = document.createElement('li');
    let pTag = document.createElement('p');
    pTag.textContent = content;

    if (author === username) {
        msgListTag.className = 'sent';
    } else {
        msgListTag.className = 'replies';
    }

    msgListTag.appendChild(pTag);
    messageElement.appendChild(msgListTag);
    chatHistory.appendChild(messageElement);
}


chatSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);

    if (Array.isArray(data['messages'])) {
        data['messages'].forEach(messageData => {
            addMessageToChat(messageData['author'], messageData['content'], username);
        });
    } else {
        let message = data['message'];
        addMessageToChat(message['author'], message['content'], username);
    }
};


chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#message-to-send').focus();
document.querySelector('#message-to-send').onkeyup = function(e) {
    if (e.key === 'Enter') {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#message-to-send');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'command': 'new_message',
        'from': username,
        'chat_id': chatID,
    }));
    messageInputDom.value = '';
};
