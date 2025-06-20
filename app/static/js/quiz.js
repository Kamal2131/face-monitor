// app/static/js/quiz.js
let quizData = {
  topic: '',
  numQuestions: 5,
  questions: [],
  userAnswers: {}
};

// Initialize quiz after proctoring starts
function initializeQuiz() {
  document.getElementById('quiz-section').style.display = 'block';
  document.getElementById('quiz-topic').textContent = quizData.topic;
  
  // Request MCQs from backend
  generateMCQs(quizData.topic, quizData.numQuestions);
}

// Generate MCQs from Groq API
async function generateMCQs(topic, count) {
  showLoader(true);
  
  try {
    const response = await fetch('/generate-mcqs', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ topic, num_questions: count })
    });
    
    if (!response.ok) throw new Error('Failed to generate questions');
    
    const data = await response.json();
    quizData.questions = data.questions;
    renderQuestions();
    startTimer(30 * 60); // 30 minutes
  } catch (error) {
    showAlert(`Quiz Error: ${error.message}`);
  } finally {
    showLoader(false);
  }
}

// Display questions
function renderQuestions() {
  const container = document.getElementById('questions-container');
  container.innerHTML = '';
  
  quizData.questions.forEach((q, index) => {
    const questionHtml = `
      <div class="card mb-3">
        <div class="card-body">
          <h5 class="card-title">Question ${index + 1}</h5>
          <p class="card-text">${q.question}</p>
          
          <div class="options-container ms-3">
            ${q.options.map((opt, optIndex) => `
              <div class="form-check mb-2">
                <input 
                  class="form-check-input" 
                  type="radio" 
                  name="question-${index}" 
                  id="q${index}-opt${optIndex}"
                  value="${String.fromCharCode(65 + optIndex)}"
                >
                <label class="form-check-label" for="q${index}-opt${optIndex}">
                  ${String.fromCharCode(65 + optIndex)}) ${opt}
                </label>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;
    container.innerHTML += questionHtml;
  });
  
  // Update question count
  document.getElementById('quiz-count').textContent = 
    `Total Questions: ${quizData.questions.length}`;
}

// Timer function
function startTimer(duration) {
  let timer = duration;
  const timerElement = document.getElementById('quiz-timer');
  
  const interval = setInterval(() => {
    const minutes = Math.floor(timer / 60);
    const seconds = timer % 60;
    
    timerElement.textContent = 
      `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
    if (--timer < 0) {
      clearInterval(interval);
      submitQuiz();
      showAlert('Time is up! Quiz submitted automatically');
    }
  }, 1000);
}

// Submit quiz
function submitQuiz() {
  // Collect user answers
  quizData.questions.forEach((_, index) => {
    const selected = document.querySelector(`input[name="question-${index}"]:checked`);
    quizData.userAnswers[index] = selected ? selected.value : null;
  });
  
  // Calculate score
  let score = 0;
  quizData.questions.forEach((q, index) => {
    if (quizData.userAnswers[index] === q.answer) {
      score++;
    }
  });
  
  // Show results
  showResults(score);
}

// Display results
function showResults(score) {
  const total = quizData.questions.length;
  const percentage = Math.round((score / total) * 100);
  
  // Update modal
  document.getElementById('score-value').textContent = score;
  document.getElementById('total-questions').textContent = total;
  
  const progress = document.getElementById('score-progress');
  progress.style.width = `${percentage}%`;
  progress.textContent = `${percentage}%`;
  
  // Set progress bar color
  if (percentage >= 80) progress.classList.add('bg-success');
  else if (percentage >= 60) progress.classList.add('bg-warning');
  else progress.classList.add('bg-danger');
  
  // Show details
  const detailsContainer = document.getElementById('results-details');
  detailsContainer.innerHTML = '';
  
  quizData.questions.forEach((q, index) => {
    const userAnswer = quizData.userAnswers[index] || 'Not answered';
    const isCorrect = userAnswer === q.answer;
    
    detailsContainer.innerHTML += `
      <div class="card mb-2 ${isCorrect ? 'border-success' : 'border-danger'}">
        <div class="card-body">
          <h6 class="card-title">Question ${index + 1}: ${q.question}</h6>
          <p class="mb-1">Your answer: ${userAnswer} ${isCorrect ? '✅' : '❌'}</p>
          <p class="mb-0 text-success">Correct answer: ${q.answer}</p>
        </div>
      </div>
    `;
  });
  
  // Show modal
  const resultsModal = new bootstrap.Modal(document.getElementById('resultsModal'));
  resultsModal.show();
}

// Helper functions
function showLoader(show) {
  const loader = document.getElementById('quiz-loader');
  if (loader) loader.style.display = show ? 'block' : 'none';
}

function showAlert(message) {
  const alert = document.createElement('div');
  alert.className = 'alert alert-warning alert-dismissible fade show';
  alert.role = 'alert';
  alert.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  `;
  
  document.querySelector('#quiz-section .card-body').prepend(alert);
}

// Initialize after proctoring starts
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('quiz-form').addEventListener('submit', (e) => {
    e.preventDefault();
    submitQuiz();
  });
  
  // Get quiz parameters from URL or form
  const urlParams = new URLSearchParams(window.location.search);
  quizData.topic = urlParams.get('topic') || 'General Knowledge';
  quizData.numQuestions = parseInt(urlParams.get('count') || 5);
  
  // Start quiz after proctoring is initialized
  setTimeout(initializeQuiz, 2000);
});