// app/static/js/proctor.js
; (async () => {
  const MODEL_PATH = '/static/models';
  const DETECT_INTERVAL = 1500;
  const MATCH_THRESHOLD = 0.6;
  let userDescriptor = null;
  let isVerifying = true;

  // Load face-api models
  await Promise.all([
    faceapi.nets.ssdMobilenetv1.loadFromUri(MODEL_PATH),
    faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_PATH),
    faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_PATH)
  ]);

  // Get current user's face descriptor from uploaded image
  async function loadUserDescriptor() {
    try {

        const res = await fetch("/api/current-user");
        const data = await res.json();

        if (data.error) {
            console.error("User fetch error:", data.error);
            return;
        }
        const imgUrl = data.image_url;  // e.g., Cloudinary URL
        const img = await faceapi.fetchImage(imgUrl);


      // Generate face descriptor
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

      const video = document.getElementById('video');
      video.srcObject = stream;
      video.style.transform = 'scaleX(-1)';

      await new Promise(resolve => video.onloadedmetadata = resolve);
      await video.play();

      return true;
    } catch (error) {
      showAlert('Camera access required!');
      console.error('Webcam error:', error);
      return false;
    }
  }

  // Face verification logic
  async function verifyFace() {
    if (!userDescriptor || !isVerifying) return;

    try {
      const detections = await faceapi.detectAllFaces(video)
        .withFaceLandmarks()
        .withFaceDescriptors();

      if (detections.length === 0) {
        updateStatus('No face detected', 'warning');
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
      } else {
        updateStatus('Unverified User ⚠️', 'error');
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

    statusElem.textContent = text;
    statusElem.className = `status-${type}`;
  }

  // Alert system
  function showAlert(message) {
    const alert = document.createElement('div');
    alert.className = 'proctor-alert';
    alert.innerHTML = `
      <div class="alert-content">
        ⚠️ ${message}
      </div>
    `;
    document.body.appendChild(alert);
    setTimeout(() => alert.remove(), 5000);
  }

  // Event reporting
  function warn(reason) {
    fetch('/api/proctor/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        events: [{
          reason,
          timestamp: new Date().toISOString()
        }]
      })
    }).catch(error => console.error('Event report failed:', error));
  }

  // Main initialization
  async function initializeProctoring() {
    // Load user's face data
    userDescriptor = await loadUserDescriptor();
    if (!userDescriptor) return;

    // Initialize camera
    if (!await initializeWebcam()) return;

    // Start verification loop
    setInterval(verifyFace, DETECT_INTERVAL);
    updateStatus('Verification Active', 'info');

    // Cleanup loading screen
    document.getElementById('loading')?.remove();
  }

  // Start the system
  initializeProctoring();
})();

