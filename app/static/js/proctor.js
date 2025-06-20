// app/static/js/proctor.js
; (async () => {
  const MODEL_PATH = '/static/models';
  const DETECT_INTERVAL = 1500;
  const MATCH_THRESHOLD = 0.6;
  let userDescriptor = null;
  let isVerifying = true;
  let tabActive = true;
  let examData = { topic: '', questions: [] };
  let successCount = 0;
  let warningCount = 0;
  let processorVideo = null;
  let floatingVideo = null;

  // Create hidden video element for processing
  function createProcessorVideo() {
    processorVideo = document.createElement('video');
    processorVideo.id = 'video-processor';
    processorVideo.autoplay = true;
    processorVideo.playsinline = true;
    processorVideo.style.display = 'none';
    document.body.appendChild(processorVideo);
    return processorVideo;
  }

  // Create floating video element
  function createFloatingVideo() {
    const container = document.getElementById('floating-video-container');
    container.style.display = 'block';
    
    floatingVideo = document.getElementById('floating-video');
    return floatingVideo;
  }

  // Get current user's face descriptor
  async function loadUserDescriptor() {
    try {
      const res = await fetch("/api/current-user");
      const data = await res.json();

      if (data.error) {
        console.error("User fetch error:", data.error);
        return null;
      }
      
      const imgUrl = data.image_url;
      const img = await faceapi.fetchImage(imgUrl);

      const detection = await faceapi.detectSingleFace(img)
        .withFaceLandmarks()
        .withFaceDescriptor();

      if (!detection) {
        showAlert('No face found in registration photo!');
        return null;
      }

      return detection.descriptor;
    } catch (error) {
      console.error('Descriptor load failed:', error);
      showAlert('Face recognition system error');
      return null;
    }
  }

  // Initialize webcam
  async function initializeWebcam() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: 'user'
        }
      });

      // Create video elements if needed
      if (!processorVideo) createProcessorVideo();
      if (!floatingVideo) createFloatingVideo();
      
      // Assign stream to both videos
      processorVideo.srcObject = stream;
      floatingVideo.srcObject = stream;

      // Play the videos
      await new Promise(resolve => processorVideo.onloadedmetadata = resolve);
      await processorVideo.play();
      
      await new Promise(resolve => floatingVideo.onloadedmetadata = resolve);
      await floatingVideo.play();

      return true;
    } catch (error) {
      showAlert('Camera access required!');
      console.error('Webcam error:', error);
      return false;
    }
  }

  // Face verification logic
  async function verifyFace() {
    if (!userDescriptor || !isVerifying || !tabActive) return;

    try {
      const detections = await faceapi.detectAllFaces(processorVideo)
        .withFaceLandmarks()
        .withFaceDescriptors();

      if (detections.length === 0) {
        updateStatus('No face detected', 'warning');
        warningCount++;
        return warn('no_face_detected');
      }

      let isMatch = false;
      for (const detection of detections) {
        const distance = faceapi.euclideanDistance(
          userDescriptor,
          detection.descriptor
        );

        if (distance <= MATCH_THRESHOLD) {
          isMatch = true;
          break;
        }
      }

      if (isMatch) {
        updateStatus('Identity Verified ✅', 'success');
        successCount++;
      } else {
        updateStatus('Unverified User ⚠️', 'error');
        warningCount++;
        warn('unverified_face_detected');
      }
    } catch (error) {
      console.error('Verification error:', error);
    }
  }

  // Status updates
  function updateStatus(text, type) {
    const statusElem = document.getElementById('verification-status');
    if (!statusElem) return;

    // Map types to Bootstrap classes
    const typeMap = {
      success: 'alert-success',
      warning: 'alert-warning',
      error: 'alert-danger',
      info: 'alert-info'
    };
    
    statusElem.textContent = text;
    statusElem.className = `alert ${typeMap[type] || 'alert-info'}`;
  }

  // Alert system
  function showAlert(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-warning alert-dismissible fade show';
    alert.role = 'alert';
    alert.innerHTML = `
      <strong>⚠️ Alert:</strong> ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.proctoring-container');
    if (container) {
      container.prepend(alert);
    }
  }

  // Event reporting
  function warn(reason) {
    const eventData = {
      events: [{
        reason,
        timestamp: new Date().toISOString(),
        exam_topic: examData.topic,
        question_numbers: examData.questions.join(', ')
      }]
    };

    fetch('/api/proctor/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(eventData)
    }).catch(error => console.error('Event report failed:', error));
  }

  // Tab visibility handler
  function handleVisibilityChange() {
    if (document.visibilityState === 'hidden') {
      tabActive = false;
      updateStatus('Tab Switch Detected! ⚠️', 'error');
      warn('tab_switch');
    } else {
      tabActive = true;
      updateStatus('Verification Active', 'info');
    }
  }

  // Collect exam data from user
  function setupExamData() {
    const topicInput = document.getElementById('exam-topic');
    const questionsInput = document.getElementById('question-numbers');
    const numQuestionsInput = document.getElementById('num-questions');
    const startBtn = document.getElementById('start-exam-btn');
    const currentTopic = document.getElementById('current-topic');
    const currentQuestions = document.getElementById('current-questions');
    
    if (!topicInput || !questionsInput || !startBtn) return;
    
    startBtn.addEventListener('click', () => {
      examData.topic = topicInput.value.trim();
      
      // Parse question numbers
      examData.questions = questionsInput.value
        .split(',')
        .map(q => q.trim())
        .filter(q => q);
      
      const numQuestions = parseInt(numQuestionsInput.value) || 5;
      
      if (!examData.topic || examData.questions.length === 0) {
        showAlert('Please enter both topic and question numbers');
        return;
      }
      
      // Update UI with exam info
      if (currentTopic) currentTopic.textContent = examData.topic;
      if (currentQuestions) currentQuestions.textContent = examData.questions.join(', ');
      
      // Switch views
      document.getElementById('exam-setup').classList.add('d-none');
      document.getElementById('proctor-section').classList.remove('d-none');
      
      // Start proctoring
      initializeProctoring();
      
      // Start quiz with the requested number of questions
      startQuiz(examData.topic, numQuestions);
    });
  }

  // Main initialization
  async function initializeProctoring() {
    // Add tab switch detection
    document.addEventListener('visibilitychange', handleVisibilityChange);
    
    // Setup exam data collection
    setupExamData();
    
    // Load user's face data
    userDescriptor = await loadUserDescriptor();
    if (!userDescriptor) return;

    // Initialize camera
    if (!await initializeWebcam()) return;

    // Start verification loop
    setInterval(verifyFace, DETECT_INTERVAL);
    updateStatus('Verification Active', 'info');
  }

  // Start the system
  initializeProctoring();
})();