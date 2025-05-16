// const video = document.getElementById('video');

// console.log("Loading models...");

// Promise.all([
//   faceapi.nets.tinyFaceDetector.loadFromUri('/static/models'),
//   faceapi.nets.faceLandmark68Net.loadFromUri('/static/models'),
//   faceapi.nets.faceRecognitionNet.loadFromUri('/static/models')
// ]).then(() => {
//   console.log("Models loaded");
//   startVideo();  // or whatever follows
// }).catch(err => console.error("Model loading error:", err));


// // video.addEventListener('play', () => {
// //   const canvas = faceapi.createCanvasFromMedia(video);
// //   document.body.append(canvas);
// //   const displaySize = { width: video.width, height: video.height };
// //   faceapi.matchDimensions(canvas, displaySize);

// //   setInterval(async () => {
// //     const detections = await faceapi.detectAllFaces(
// //       video, new faceapi.TinyFaceDetectorOptions()
// //     );

// //     canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
// //     faceapi.draw.drawDetections(canvas, faceapi.resizeResults(detections, displaySize));

// //     if (detections.length === 0) {
// //       sendWarning("No face detected");
// //     } else if (detections.length > 1) {
// //       sendWarning("Multiple faces detected");
// //     } else {
// //       const box = detections[0].box;
// //       if (box.width < 100 || box.height < 100) {
// //         sendWarning("Face not centered properly");
// //       }
// //     }

// //   }, 3000);
// // });

// video.addEventListener('loadedmetadata', () => {
//   const canvas = faceapi.createCanvasFromMedia(video);
//   document.body.append(canvas);
//   const displaySize = { width: video.videoWidth, height: video.videoHeight };
//   faceapi.matchDimensions(canvas, displaySize);

//   setInterval(async () => {
//     const detections = await faceapi.detectAllFaces(
//       video, new faceapi.TinyFaceDetectorOptions()
//     );

//     canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
//     faceapi.draw.drawDetections(canvas, faceapi.resizeResults(detections, displaySize));

//     if (detections.length === 0) {
//       sendWarning("No face detected");
//     } else if (detections.length > 1) {
//       sendWarning("Multiple faces detected");
//     } else {
//       const box = detections[0].box;
//       if (box.width < 100 || box.height < 100) {
//         sendWarning("Face not centered properly");
//       }
//     }

//   }, 3000);
// });

// function showAlert(reason) {
//   let alertBox = document.getElementById("alertBox");
//   if (!alertBox) {
//     alertBox = document.createElement("div");
//     alertBox.id = "alertBox";
//     alertBox.style.cssText = "position:fixed;top:10px;right:10px;background:red;color:white;padding:10px;border-radius:5px;z-index:1000;";
//     document.body.appendChild(alertBox);
//   }
//   alertBox.innerText = reason;
// }


// function sendWarning(reason) {
//   showAlert(reason);  // Show on UI

//   fetch('/raise-warning', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({
//       reason: reason,
//       timestamp: new Date().toISOString()
//     })
//   }).then(res => {
//     if (!res.ok) {
//       console.error('Warning failed to send');
//     }
//   });
// }



// const video = document.getElementById('video');
// const warning = document.getElementById('warning');

// Promise.all([
//   faceapi.nets.tinyFaceDetector.loadFromUri('/static/models'),
//   faceapi.nets.faceLandmark68Net.loadFromUri('/static/models'),
//   faceapi.nets.faceRecognitionNet.loadFromUri('/static/models')
// ]).then(() => {
//   console.log("Models loaded");
//   startVideo();
// });

// function startVideo() {
//   navigator.mediaDevices.getUserMedia({ video: {} })
//     .then(stream => video.srcObject = stream)
//     .catch(err => console.error("Webcam error:", err));
// }

// video.addEventListener('play', () => {
//   const canvas = document.getElementById('overlay');
//   const displaySize = { width: video.width, height: video.height };
//   faceapi.matchDimensions(canvas, displaySize);

//   const options = new faceapi.TinyFaceDetectorOptions({ inputSize: 512, scoreThreshold: 0.5 });

//   setInterval(async () => {
//     const detections = await faceapi.detectAllFaces(video, options);
//     const resized = faceapi.resizeResults(detections, displaySize);

//     canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
//     faceapi.draw.drawDetections(canvas, resized);

//     if (resized.length === 0) {
//       warning.innerText = "⚠️ No face detected";
//     } else {
//       warning.innerText = ""; // Clear warning
//     }
//   }, 1000);
// });


// ------------------------------------------------------------>
// New Code generated

const video = document.getElementById('video');

console.log("Loading models...");

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri('/static/models'),
  faceapi.nets.faceLandmark68Net.loadFromUri('/static/models'),
  faceapi.nets.faceRecognitionNet.loadFromUri('/static/models')
]).then(() => {
  console.log("Models loaded");
  startVideo();
}).catch(err => console.error("Model loading error:", err));

function startVideo() {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      video.srcObject = stream;
      video.play();
    })
    .catch(err => {
      console.error("Failed to access webcam:", err);
    });
}

video.addEventListener('play', () => {
  const canvas = faceapi.createCanvasFromMedia(video);
  document.body.appendChild(canvas);
  const displaySize = { width: video.videoWidth, height: video.videoHeight };
  faceapi.matchDimensions(canvas, displaySize);

  setInterval(async () => {
    const detections = await faceapi.detectAllFaces(
      video,
      new faceapi.TinyFaceDetectorOptions()
    );

    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    faceapi.draw.drawDetections(canvas, resizedDetections);

    if (detections.length === 0) {
      sendWarning("No face detected");
    } else if (detections.length > 1) {
      sendWarning("Multiple faces detected");
    } else {
      const box = detections[0].box;
      if (box.width < 100 || box.height < 100) {
        sendWarning("Face not centered properly");
      }
    }
  }, 3000);
});

video.addEventListener('loadedmetadata', () => {
  const canvas = faceapi.createCanvasFromMedia(video);
  document.body.append(canvas);
  const displaySize = { width: video.videoWidth, height: video.videoHeight };
  faceapi.matchDimensions(canvas, displaySize);

  setInterval(async () => {
    // Use the more accurate SSD Mobilenet v1 detector with min confidence 0.5
    const detections = await faceapi.detectAllFaces(
      video,
      new faceapi.SsdMobilenetv1Options({ minConfidence: 0.5 })
    );

    console.log('Detections:', detections);

    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    faceapi.draw.drawDetections(canvas, resizedDetections);

    if (detections.length === 0) {
      sendWarning("No face detected");
    } else if (detections.length > 1) {
      sendWarning("Multiple faces detected");
    } else {
      const box = detections[0].box;
      // Commented out temporarily to reduce false warnings during debugging
      // if (box.width < 100 || box.height < 100) {
      //   sendWarning("Face not centered properly");
      // }
    }

  }, 3000);
});


function showAlert(reason) {
  let alertBox = document.getElementById("alertBox");
  if (!alertBox) {
    alertBox = document.createElement("div");
    alertBox.id = "alertBox";
    alertBox.style.cssText = "position:fixed;top:10px;right:10px;background:red;color:white;padding:10px;border-radius:5px;z-index:1000;";
    document.body.appendChild(alertBox);
  }
  alertBox.innerText = reason;
}

function sendWarning(reason) {
  showAlert(reason);  // Show warning on UI

  fetch('/raise-warning', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      reason: reason,
      timestamp: new Date().toISOString()
    })
  }).then(res => {
    if (!res.ok) {
      console.error('Warning failed to send');
    }
  });
}
