document.addEventListener('DOMContentLoaded', () => {
  if (typeof ticket_id !== 'undefined') {
    console.log(`Iniciando a sala com ticket_id: ${ticket_id}`)
    startMessageStream(ticket_id)
  } else {
    console.error('ticket_id não está definido no DOM.')
  }

  const sendButton = document.getElementById('sendButton')
  const messageInput = document.getElementById('messageInput')
  const recordButton = document.getElementById('recordButton')
  const stopButton = document.getElementById('stopButton')
  const audioRecordingDiv = document.getElementById('audioRecording')

  let mediaRecorder
  let audioChunks = []

  if (sendButton && messageInput) {
    sendButton.addEventListener('click', sendMessage)
  } else {
    console.error('Elementos sendButton ou messageInput não encontrados.')
  }

  if (recordButton && stopButton) {
    recordButton.addEventListener('click', startRecording)
    stopButton.addEventListener('click', stopRecording)
  } else {
    console.error('Botões de gravação de áudio não encontrados.')
  }

  function sendMessage() {
    const message = messageInput.value.trim()
    if (!message) {
      alert('Digite uma mensagem antes de enviar.')
      return
    }

    fetch(`${ticket_id}/send/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ message: message }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === 'ok') {
          console.log('Mensagem enviada:', data.message)
          messageInput.value = '' // Limpa o input
        } else {
          console.error('Erro ao enviar mensagem:', data.error)
        }
      })
      .catch((error) =>
        console.error('Erro na comunicação com o servidor:', error)
      )
  }

  function startMessageStream(ticket_id) {
    const messagesContainer = document.getElementById('messages')

    if (!messagesContainer) {
      console.error('Elemento messagesContainer não encontrado.')
      return
    }

    const eventSource = new EventSource(`${ticket_id}/stream/`)

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data)
      const messageElement = document.createElement('div')

      messageElement.className =
        'message ' +
        (data.sender === 'user' ? 'user-message' : 'attendant-message')

      messageElement.textContent = `${data.sender_name}: ${data.message}`
      messagesContainer.appendChild(messageElement)
      messagesContainer.scrollTop = messagesContainer.scrollHeight // Scroll automático
    }

    eventSource.onerror = (error) => {
      console.error('Erro no stream de mensagens:', error)
      eventSource.close()
    }
  }

  /*** GRAVAÇÃO DE ÁUDIO ***/
  function startRecording() {
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        mediaRecorder = new MediaRecorder(stream)
        audioChunks = []

        mediaRecorder.ondataavailable = (event) => {
          audioChunks.push(event.data)
        }

        mediaRecorder.onstop = () => {
          processAndSendAudio()
        }

        mediaRecorder.start()
        console.log('Gravação iniciada...')

        // Corrigindo visibilidade dos botões
        audioRecordingDiv.style.display = 'block'
        recordButton.style.display = 'none'

        // Exibe o botão "Parar" de gravação
        stopButton.classList.add('active') // Adiciona a classe "active" para mostrar o botão
        stopButton.style.display = 'block' // Garante que o botão de parar seja visível
      })
      .catch((error) => console.error('Erro ao acessar microfone:', error))
  }

  function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop()
      console.log('Gravação finalizada.')

      // Ajustando visibilidade dos botões
      audioRecordingDiv.style.display = 'none'
      recordButton.style.display = 'block'
    }
  }

  function processAndSendAudio() {
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' })
    const formData = new FormData()
    formData.append('audio', audioBlob, 'audio.wav')

    console.log('Enviando áudio:', audioBlob)

    fetch(`${ticket_id}/send-audio/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === 'ok') {
          console.log('Áudio enviado com sucesso:', data.audio_url)

          // Adicionando um player de áudio para reprodução
          const audioPlayer = document.createElement('audio')
          audioPlayer.controls = true
          audioPlayer.src = data.audio_url // Usando a URL do áudio retornada
          document.getElementById('messages').appendChild(audioPlayer) // Adicionando o player à área de mensagens
        } else {
          console.error('Erro ao enviar áudio:', data.message)
        }
      })
      .catch((error) => {
        console.error('Erro ao enviar áudio:', error)
      })
  }

  function getCookie(name) {
    let cookieValue = null
    if (document.cookie) {
      document.cookie.split(';').forEach((cookie) => {
        cookie = cookie.trim()
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        }
      })
    }
    return cookieValue
  }
})
