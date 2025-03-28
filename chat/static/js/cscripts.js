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

document.addEventListener("DOMContentLoaded", () => {
  if (typeof ticket_id !== "undefined") {
    console.log(`Iniciando a sala com ticket_id: ${ticket_id}`);
    startMessageStream(ticket_id);
  } else {
    console.error("ticket_id não está definido no DOM.");
  }

  const inputField = document.getElementById("chat-input");
  const previewImg = document.getElementById("image-preview"); // Elemento <img> para exibir preview
  setupPasteUpload(inputField, previewImg); // Configura o upload de imagem via paste

  const sendButton = document.getElementById("sendButton");
  const messageInput = document.getElementById("messageInput");
  const recordButton = document.getElementById("recordButton");
  const stopButton = document.getElementById("stopButton");
  const audioRecordingDiv = document.getElementById("audioRecording");

  let mediaRecorder;
  let audioChunks = [];

  if (sendButton && messageInput) {
    sendButton.addEventListener("click", sendMessage);
  } else {
    console.error("Elementos sendButton ou messageInput não encontrados.");
  }

  if (recordButton && stopButton) {
    recordButton.addEventListener("click", startRecording);
    stopButton.addEventListener("click", stopRecording);
  } else {
    console.error("Botões de gravação de áudio não encontrados.");
  }

  function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) {
      alert("Digite uma mensagem antes de enviar.");
      return;
    }

    fetch(`${ticket_id}/send/`, {
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
          console.log("Mensagem enviada:", data.message);
          messageInput.value = ""; // Limpa o input
        } else {
          console.error("Erro ao enviar mensagem:", data.error);
        }
      })
      .catch((error) =>
        console.error("Erro na comunicação com o servidor:", error)
      );
  }

  function startMessageStream(ticket_id) {
    const messagesContainer = document.getElementById("messages");

    if (!messagesContainer) {
      console.error("Elemento messagesContainer não encontrado.");
      return;
    }

    const eventSource = new EventSource(`${ticket_id}/stream/`);

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const messageElement = document.createElement("div");
      const senderClass =
        data.sender === "user" ? "user-message" : "attendant-message";

      messageElement.className = "message " + senderClass;

      // Exibe a mensagem de texto
      const messageText = document.createElement("span");
      messageText.textContent = `${data.sender_name}: ${data.message}`;
      messageElement.appendChild(messageText);

      // Alinha as mensagens dependendo do remetente
      if (data.sender === "user") {
        messageElement.style.textAlign = "left";
        messageElement.style.marginLeft = "10px"; // Ajusta a margem à esquerda
      } else {
        messageElement.style.textAlign = "right";
        messageElement.style.marginRight = "10px"; // Ajusta a margem à direita
      }

      messagesContainer.appendChild(messageElement);
      messagesContainer.scrollTop = messagesContainer.scrollHeight; // Scroll automático
    };

    eventSource.onerror = (error) => {
      console.error("Erro no stream de mensagens:", error);
      eventSource.close();
    };
  }

  /*** GRAVAÇÃO DE ÁUDIO ***/
  function startRecording() {
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
          audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
          processAndSendAudio();
        };

        mediaRecorder.start();
        console.log("Gravação iniciada...");

        // Ajusta a visibilidade dos botões
        audioRecordingDiv.style.display = "block";
        recordButton.style.display = "none"; // Esconde o botão de gravação
        stopButton.style.display = "inline-block"; // Exibe o botão de parar

        stopButton.classList.add("active"); // A classe "active" deixa visível o botão "Parar"
      })
      .catch((error) => console.error("Erro ao acessar microfone:", error));
  }

  function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.stop();
      console.log("Gravação finalizada.");

      // Ajusta a visibilidade dos botões
      audioRecordingDiv.style.display = "none";
      recordButton.style.display = "inline-block"; // Exibe novamente o botão de gravar
      stopButton.style.display = "none"; // Esconde o botão de parar
    }
  }

  function processAndSendAudio() {
    const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
    const formData = new FormData();
    formData.append("audio", audioBlob, "audio.wav");

    console.log("Enviando áudio:", audioBlob);

    fetch(`${ticket_id}/send-audio/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "ok") {
          console.log("Áudio enviado com sucesso:", data.audio_url);

          // Adicionando um player de áudio para reprodução
          const audioPlayer = document.createElement("audio");
          audioPlayer.controls = true;
          audioPlayer.src = data.audio_url; // Usando a URL do áudio retornada

          // Ajusta o alinhamento do player de áudio
          audioPlayer.style.float = data.sender === "user" ? "left" : "right";

          document.getElementById("messages").appendChild(audioPlayer); // Adicionando o player à área de mensagens
          document.getElementById("messages").scrollTop =
            document.getElementById("messages").scrollHeight;
        } else {
          console.error("Erro ao enviar áudio:", data.message);
        }
      })
      .catch((error) => {
        console.error("Erro ao enviar áudio:", error);
      });
  }

  // Função de upload via paste
  function setupPasteUpload(inputElement, previewElement) {
    document.addEventListener("paste", async (event) => {
      const items = (event.clipboardData || event.originalEvent.clipboardData)
        .items;

      for (const item of items) {
        if (item.type.indexOf("image") === 0) {
          const blob = item.getAsFile();

          // Enviar para o backend
          try {
            const formData = new FormData();
            formData.append("image", blob, "screenshot.png");

            const response = await fetch(`${ticket_id}/send_image/`, {
              method: "POST",
              body: formData,
              headers: {
                "X-CSRFToken": getCookie("csrftoken"),
              },
            });

            // Verificando a resposta do servidor
            const data = await response.json();
            if (response.ok && data.file_url) {
              console.log("Imagem enviada com sucesso:", data.file_url);

              // Adicionando a imagem ao chat
              const imgElement = document.createElement("img");
              imgElement.src = data.file_url; // A URL da imagem retornada pelo servidor
              imgElement.alt = "Imagem enviada";
              imgElement.style.maxWidth = "60%";

              // Ajusta a imagem conforme o remetente
              imgElement.style.float =
                data.sender === "user" ? "left" : "right";

              // Adiciona a imagem na área de mensagens
              const messagesContainer = document.getElementById("messages");
              messagesContainer.appendChild(imgElement);
              messagesContainer.scrollTop = messagesContainer.scrollHeight;

              // Função para expandir a imagem em um modal
              imgElement.addEventListener("click", () => {
                const expandedImg = document.createElement("img");
                expandedImg.src = imgElement.src;
                expandedImg.style.maxWidth = "90%";
                expandedImg.style.maxHeight = "90%";
                expandedImg.style.margin = "0 auto";
                expandedImg.style.display = "block";
                expandedImg.style.cursor = "zoom-out"; // Indicativo de que é possível fechar

                // Modal para exibir imagem expandida
                const modal = document.createElement("div");
                modal.style.position = "fixed";
                modal.style.top = "0";
                modal.style.left = "0";
                modal.style.width = "100%";
                modal.style.height = "100%";
                modal.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
                modal.style.display = "flex";
                modal.style.justifyContent = "center";
                modal.style.alignItems = "center";
                modal.style.zIndex = "1000";
                modal.addEventListener("click", () => {
                  modal.remove();
                });

                modal.appendChild(expandedImg);
                document.body.appendChild(modal);
              });
            } else {
              console.error(
                "Erro ao enviar imagem:",
                data.error || "Erro desconhecido"
              );
            }
          } catch (error) {
            console.error("Erro ao enviar imagem:", error);
          }
        }
      }
    });
  }
});
