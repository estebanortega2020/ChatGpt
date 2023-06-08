css = '''
<style>
body {
    background-image: url('https://img.freepik.com/vector-gratis/fondo-negro-degradado-texturas-doradas_52683-76896.jpg');
    background-size: cover;
    background-position: center center;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    min-height: 100vh;
    font-family: 'Lato', sans-serif;
    margin: 0 0 50px;
    position: relative;
    z-index: -1;
    opacity: 0.65; /* Cambia el valor para ajustar la opacidad */
}

.chat-container {
    overflow-y: scroll;
    scroll-behavior: smooth;
    max-height: 400px; /* Ajusta la altura máxima según tus necesidades */
}

.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
}

.chat-message.user {
    background-color: #07472e;
}

.chat-message.bot {
    background-color: #252a35;
}

.chat-message .avatar {
    width: 20%;
}

.chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
}

.chat-message .message {
    width: 80%;
    padding: 0 1.5rem;
    color: #fff;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://static.vecteezy.com/system/resources/previews/010/054/157/non_2x/chat-bot-robot-avatar-in-circle-round-shape-isolated-on-white-background-stock-illustration-ai-technology-futuristic-helper-communication-conversation-concept-in-flat-style-vector.jpg" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://media.gq.com.mx/photos/5be9ccf8a57669ea79b4c954/1:1/w_1189,h_1189,c_limit/cristiano_ronaldo_reality_facebook_7107.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''