// app/static/js/proctor.js
;(async () => {
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
      // Get current username
      const userRes = await fetch('/api/current-user');
      const { name } = await userRes.json();
      
      // Load registered face image
      const img = await faceapi.fetchImage(`/static/uploads/${name}.jpg`);
      
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
// // app/static/js/proctor.js
// ;(async () => {
//   const MODEL_PATH = '/static/models';
//   const DETECT_INTERVAL = 1500;
//   const FLUSH_INTERVAL = 10000;
//   let isDetecting = false;
//   let faceDetector;

//   // UI Elements
//   const video = document.getElementById('video');
//   const statusElement = document.getElementById('status');

//   // ***********************
//   // Model Initialization
//   // ***********************

//   async function initializeModels() {
//     try {
//       // Try loading SSD Mobilenet first
//       await faceapi.nets.ssdMobilenetv1.loadFromUri(MODEL_PATH);
//       faceDetector = new faceapi.SsdMobilenetv1Options({
//         minConfidence: 0.5
//       });
//       console.log('Using SSD Mobilenet detector');
      
//       // Fallback to Tiny Face Detector if SSD fails
//     } catch {
//       console.log('Falling back to Tiny Face Detector');
//       await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_PATH);
//       faceDetector = new faceapi.TinyFaceDetectorOptions({
//         inputSize: 512,
//         scoreThreshold: 0.4
//       });
//     }

//     // Load additional models
//     await Promise.all([
//       faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_PATH),
//       faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_PATH)
//     ]);

//     updateStatus('All models loaded ✅', 'success');
//     return true;
//   }

//   // ***********************
//   // Webcam Setup
//   // ***********************

//   async function initializeWebcam() {
//     try {
//       const stream = await navigator.mediaDevices.getUserMedia({
//         video: {
//           width: { ideal: 1280 },
//           height: { ideal: 720 },
//           facingMode: 'user'
//         }
//       });

//       video.srcObject = stream;
//       video.style.transform = 'scaleX(-1)';
      
//       await new Promise(resolve => {
//         video.onloadedmetadata = () => {
//           video.width = video.videoWidth;
//           video.height = video.videoHeight;
//           resolve();
//         };
//       });

//       await video.play();
//       return true;
//     } catch (error) {
//       showAlert('Camera access required!');
//       console.error('Webcam error:', error);
//       return false;
//     }
//   }

//   // ***********************
//   // Detection Core
//   // ***********************

//   function startDetection() {
//     const canvas = faceapi.createCanvasFromMedia(video);
//     document.body.appendChild(canvas);
//     faceapi.matchDimensions(canvas, video);

//     const detectionLoop = async () => {
//       if (!isDetecting) return;

//       try {
//         const detections = await faceapi.detectAllFaces(video, faceDetector)
//           .withFaceLandmarks()
//           .withFaceDescriptors();

//         canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
//         const resized = faceapi.resizeResults(detections, video);
        
//         // Draw detection visuals
//         faceapi.draw.drawDetections(canvas, resized);
//         faceapi.draw.drawFaceLandmarks(canvas, resized);

//         // Handle detection results
//         if (resized.length === 0) {
//           handleDetectionEvent('no_face_detected');
//         } else if (resized.length > 1) {
//           handleDetectionEvent('multiple_faces_detected');
//         } else {
//           updateStatus('Face detected ✅', 'success');
//         }
//       } catch (error) {
//         console.error('Detection error:', error);
//       }
      
//       setTimeout(detectionLoop, DETECT_INTERVAL);
//     };

//     detectionLoop();
//   }

//   // ***********************
//   // Event Handling
//   // ***********************

//   function handleDetectionEvent(reason) {
//     const event = {
//       reason,
//       timestamp: new Date().toISOString()
//     };
//     bufferEvent(event);
//     showAlert(reason);
//     updateStatus(reason.replace(/_/g, ' ') + ' ⚠️', 'warning');
//   }

//   const eventBuffer = [];
//   function bufferEvent(event) {
//     eventBuffer.push(event);
//     if (eventBuffer.length >= 5) flushEvents();
//   }

//   async function flushEvents() {
//     if (eventBuffer.length === 0) return;
    
//     try {
//       const response = await fetch('/api/proctor/events', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ events: eventBuffer.splice(0) })
//       });
      
//       if (!response.ok) throw new Error('Flush failed');
//     } catch (error) {
//       console.error('Event flush error:', error);
//     }
//   }

//   // ***********************
//   // UI Helpers
//   // ***********************

//   function updateStatus(text, type = 'info') {
//     if (!statusElement) return;
//     statusElement.innerHTML = `
//       <div class="status-${type}">
//         ${text}
//       </div>
//     `;
//   }

//   function showAlert(message) {
//     const alert = document.createElement('div');
//     alert.className = 'proctor-alert';
//     alert.innerHTML = `
//       <div class="alert-content">
//         ⚠️ ${message.replace(/_/g, ' ')}
//       </div>
//     `;
//     document.body.appendChild(alert);
//     setTimeout(() => alert.remove(), 5000);
//   }

//   // ***********************
//   // Main Initialization
//   // ***********************

//   async function initializeProctoring() {
//     try {
//       // Load core components
//       if (!await initializeModels()) return;
//       if (!await initializeWebcam()) return;

//       // Start detection system
//       isDetecting = true;
//       startDetection();
//       setInterval(flushEvents, FLUSH_INTERVAL);

//       // Setup event listeners
//       document.addEventListener('visibilitychange', () => 
//         handleDetectionEvent(document.hidden ? 'tab_hidden' : 'tab_visible')
//       );
//       window.addEventListener('blur', () => handleDetectionEvent('window_blur'));
      
//       // Cleanup loading screen
//       document.getElementById('loading')?.remove();

//     } catch (error) {
//       console.error('Initialization failed:', error);
//       showAlert('System startup error!');
//     }
//   }

//   // Start proctoring system
//   initializeProctoring();
// })();