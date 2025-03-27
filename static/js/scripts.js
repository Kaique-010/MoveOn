/*const ticketId = "{{ ticket_id }}"; // Pegamos o ID do ticket vindo do Django

    let mediaRecorder;
    let audioChunks = [];

    // Função para enviar mensagem
    document
      .getElementById("sendButton")
      .addEventListener("click", function () {
        const message = document.getElementById("messageInput").value;
        if (message.trim() === "") return; // Evita mensagens vazias

        fetch(`/chat/${ticketId}/send/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: JSON.stringify({ message: message }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "ok") {
              addMessageToChat(data.message, data.sender, data.sender_name);
              document.getElementById("messageInput").value = ""; // Limpa o campo
            }
          })
          .catch((error) => console.error("Erro ao enviar mensagem:", error));
      });

    // Função para gravar áudio
    document
      .getElementById("recordButton")
      .addEventListener("click", startRecording);
    document
      .getElementById("stopButton")
      .addEventListener("click", stopRecording);

    function startRecording() {
      document.getElementById("audioRecording").classList.add("active");
      navigator.mediaDevices
        .getUserMedia({ audio: true })
        .then((stream) => {
          mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.start();

          mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
          };

          mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
            const audioUrl = URL.createObjectURL(audioBlob);
            sendAudio(audioUrl);
          };
        })
        .catch((err) => console.error("Erro ao acessar o microfone: ", err));
    }

    function stopRecording() {
      mediaRecorder.stop();
      document.getElementById("audioRecording").classList.remove("active");
    }

    // Função para enviar áudio
    function sendAudio(audioUrl) {
      fetch(`/chat/${ticketId}/send-audio/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ audio: audioUrl }), // Envia a URL do áudio
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "ok") {
            addMessageToChat(
              "Áudio enviado!",
              data.sender,
              data.sender_name,
              audioUrl
            );
          }
        })
        .catch((error) => console.error("Erro ao enviar áudio:", error));
    }

    // Função para adicionar a mensagem no chat
    function addMessageToChat(text, sender, senderName, audioUrl) {
      const messagesContainer = document.getElementById("messages");
      const messageElement = document.createElement("div");

      // Adiciona o nome do remetente acima da mensagem
      const senderElement = document.createElement("p");
      senderElement.textContent = senderName;
      senderElement.classList.add("message-sender");
      messageElement.appendChild(senderElement);

      // Adiciona o texto ou áudio à mensagem
      if (audioUrl) {
        const audioElement = document.createElement("audio");
        audioElement.controls = true;
        audioElement.src = audioUrl;
        messageElement.appendChild(audioElement);
      } else {
        const messageText = document.createElement("p");
        messageText.textContent = text;
        messageElement.appendChild(messageText);
      }

      // Adiciona a classe do remetente
      if (sender === "user") {
        messageElement.classList.add("message", "user-message");
      } else {
        messageElement.classList.add("message", "attendant-message");
      }

      messagesContainer.appendChild(messageElement);
      messagesContainer.scrollTop = messagesContainer.scrollHeight; // Rola para baixo
    }

    // Obtém CSRF token do cookie
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie) {
        document.cookie.split(";").forEach((cookie) => {
          cookie = cookie.trim();
          if (cookie.startsWith(name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          }
        });
      }
      return cookieValue;
    }

    // Iniciar a conexão com o servidor para ouvir mensagens
    const eventSource = new EventSource(`/chat/${ticketId}/stream/`);

    eventSource.onmessage = function (event) {
      const data = JSON.parse(event.data);

      // Adiciona a mensagem no chat
      addMessageToChat(data.message, data.sender, data.sender_name);
    };*/
