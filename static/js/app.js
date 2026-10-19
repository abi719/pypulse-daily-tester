/**
 * PyPulse Daily Application Controller
 * Manages Auth, Daily 5-Question Test Sessions, 45-Min Timer, Grading,
 * Skill Progression Hub, and Mentor Review Dashboard.
 */

// Global State
window.currentUser = null;
window.currentTestState = null;
window.currentQuestionIndex = 0;
window.timerInterval = null;
let isRegisterMode = false;

// ----------------- Initialization -----------------

document.addEventListener('DOMContentLoaded', () => {
  // Check for saved user session in localStorage
  const savedUser = localStorage.getItem('pypulse_user');
  if (savedUser) {
    try {
      window.currentUser = JSON.parse(savedUser);
      updateUserHeader();
      // Load user's test or dashboard
      if (window.currentUser.role === 'mentor') {
        showSection('mentor-section');
      } else {
        loadDailyTest();
      }
    } catch (e) {
      localStorage.removeItem('pypulse_user');
      showSection('auth-section');
    }
  } else {
    showSection('auth-section');
  }
});

// ----------------- Navigation & Section Switching -----------------

function showSection(sectionId) {
  const sections = ['auth-section', 'test-section', 'results-section', 'progress-section', 'mentor-section'];
  sections.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.add('hidden');
  });

  const activeEl = document.getElementById(sectionId);
  if (activeEl) activeEl.classList.remove('hidden');

  // Update Nav tab styling
  document.querySelectorAll('.nav-tab').forEach(btn => btn.classList.remove('active'));
  if (sectionId === 'test-section') document.getElementById('nav-daily-test')?.classList.add('active');
  if (sectionId === 'progress-section') {
    document.getElementById('nav-progress')?.classList.add('active');
    loadSkillProgressHub();
  }
  if (sectionId === 'mentor-section') {
    document.getElementById('nav-mentor')?.classList.add('active');
    loadMentorDashboard();
  }

  // Update mobile bottom nav tab styling
  document.querySelectorAll('.nav-tab-mobile').forEach(btn => {
    btn.classList.remove('text-brand-400');
    btn.classList.add('text-slate-400');
  });
  if (sectionId === 'test-section') document.getElementById('m-nav-test')?.classList.replace('text-slate-400', 'text-brand-400');
  if (sectionId === 'progress-section') document.getElementById('m-nav-progress')?.classList.replace('text-slate-400', 'text-brand-400');
  if (sectionId === 'mentor-section') document.getElementById('m-nav-mentor')?.classList.replace('text-slate-400', 'text-brand-400');

  // Toggle header timer visibility: only show during active test
  const timerContainer = document.getElementById('header-timer-container');
  if (timerContainer) {
    if (sectionId === 'test-section' && window.currentTestState && window.currentTestState.status === 'in_progress') {
      timerContainer.classList.remove('hidden');
      timerContainer.classList.add('flex');
    } else {
      timerContainer.classList.add('hidden');
      timerContainer.classList.remove('flex');
    }
  }
}

function navigateHome() {
  if (!window.currentUser) {
    showSection('auth-section');
  } else if (window.currentUser.role === 'mentor') {
    showSection('mentor-section');
  } else {
    showSection('test-section');
  }
}

// ----------------- Authentication -----------------

function toggleAuthMode() {
  isRegisterMode = !isRegisterMode;
  const title = document.getElementById('auth-title');
  const subtitle = document.getElementById('auth-subtitle');
  const nameGroup = document.getElementById('name-field-group');
  const submitBtn = document.getElementById('auth-submit-btn');
  const togglePrompt = document.getElementById('auth-toggle-prompt');
  const toggleBtn = document.getElementById('auth-toggle-btn');
  const errorMsg = document.getElementById('auth-error-msg');
  errorMsg.classList.add('hidden');

  if (isRegisterMode) {
    title.textContent = 'Create Student Account';
    subtitle.textContent = 'Join the daily Python coding journey';
    nameGroup.classList.remove('hidden');
    submitBtn.textContent = 'Register & Start Day 1';
    togglePrompt.textContent = 'Already have an account?';
    toggleBtn.textContent = 'Sign In';
  } else {
    title.textContent = 'Sign In to PyPulse';
    subtitle.textContent = 'Start your 45-minute daily 5-question Python challenge';
    nameGroup.classList.add('hidden');
    submitBtn.textContent = 'Sign In & Open Arena';
    togglePrompt.textContent = "Don't have an account?";
    toggleBtn.textContent = 'Create an account';
  }
}

function quickFillCredentials(username, password) {
  if (isRegisterMode) toggleAuthMode();
  document.getElementById('auth-username').value = username;
  document.getElementById('auth-password').value = password;
  handleAuthSubmit(new Event('submit'));
}

async function handleAuthSubmit(e) {
  if (e && e.preventDefault) e.preventDefault();
  const username = document.getElementById('auth-username').value.trim();
  const password = document.getElementById('auth-password').value;
  const name = document.getElementById('auth-name').value.trim();
  const errorBox = document.getElementById('auth-error-msg');
  const errorText = document.getElementById('auth-error-text');

  errorBox.classList.add('hidden');

  const endpoint = isRegisterMode ? '/api/auth/register' : '/api/auth/login';
  const payload = isRegisterMode ? { username, password, name: name || username, role: 'student' } : { username, password };

  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (data.success && data.user) {
      window.currentUser = data.user;
      localStorage.setItem('pypulse_user', JSON.stringify(data.user));
      updateUserHeader();

      if (data.user.role === 'mentor') {
        showSection('mentor-section');
      } else {
        loadDailyTest();
      }
    } else {
      errorText.textContent = data.message || 'Authentication failed.';
      errorBox.classList.remove('hidden');
    }
  } catch (err) {
    errorText.textContent = 'Network error connecting to server.';
    errorBox.classList.remove('hidden');
  }
}

function updateUserHeader() {
  const headerMenu = document.getElementById('user-header-menu');
  const loginBtn = document.getElementById('header-login-btn');
  const nameEl = document.getElementById('user-display-name');
  const roleEl = document.getElementById('user-display-role');
  const avatarEl = document.getElementById('user-avatar-initial');
  const navMentor = document.getElementById('nav-mentor');

  if (window.currentUser) {
    headerMenu.classList.remove('hidden');
    headerMenu.classList.add('flex');
    loginBtn.classList.add('hidden');

    nameEl.textContent = window.currentUser.name || window.currentUser.username;
    roleEl.textContent = window.currentUser.role;
    avatarEl.textContent = (window.currentUser.name || window.currentUser.username).charAt(0).toUpperCase();

    // Show mentor tab only if mentor or admin
    if (window.currentUser.role === 'mentor') {
      navMentor?.classList.remove('hidden');
    } else {
      navMentor?.classList.add('hidden');
    }

    // Toggle mobile bottom nav bar
    const mobileBottomNav = document.getElementById('mobile-bottom-nav');
    const mobileMentorBtn = document.getElementById('m-nav-mentor');
    if (mobileBottomNav) {
      mobileBottomNav.classList.remove('hidden');
      if (window.currentUser.role === 'mentor') {
        mobileMentorBtn?.classList.remove('hidden');
      } else {
        mobileMentorBtn?.classList.add('hidden');
      }
    }
  } else {
    headerMenu.classList.add('hidden');
    headerMenu.classList.remove('flex');
    loginBtn.classList.remove('hidden');
    document.getElementById('mobile-bottom-nav')?.classList.add('hidden');
  }
}

function handleLogout() {
  if (window.timerInterval) clearInterval(window.timerInterval);
  window.currentUser = null;
  window.currentTestState = null;
  localStorage.removeItem('pypulse_user');
  updateUserHeader();
  showSection('auth-section');
}

// ----------------- Daily Test Management -----------------

async function loadDailyTest(forceNew = false) {
  if (!window.currentUser) return showSection('auth-section');

  try {
    const res = await fetch(`/api/test/today?user_id=${window.currentUser.id}&force_new=${forceNew}`);
    const data = await res.json();

    if (data.status === 'completed_today') {
      showDailyCompletedNotice(data);
      return;
    }

    window.currentTestState = {
      session_id: data.session_id,
      day_number: data.day_number,
      questions: data.questions,
      remaining_seconds: data.remaining_seconds,
      status: data.status,
      answers: {},
      question_statuses: {}
    };

    // Prepopulate saved draft answers if any
    if (data.saved_submissions) {
      Object.entries(data.saved_submissions).forEach(([qid, sub]) => {
        window.currentTestState.answers[qid] = sub.code;
        if (sub.is_correct) window.currentTestState.question_statuses[qid] = 'solved';
      });
    }

    document.getElementById('arena-day-badge').textContent = `DAY ${data.day_number}`;

    // Render 5 Q-pills
    renderQuestionPills();

    // Switch to first question
    switchQuestion(0);

    // Start 45-minute countdown timer
    startCountdownTimer(data.remaining_seconds);

    showSection('test-section');
  } catch (err) {
    console.error('Failed to load daily test', err);
    alert('Error loading today\'s test. Please check the server connection.');
  }
}

function showDailyCompletedNotice(data) {
  showSection('results-section');
  document.getElementById('result-day-num').textContent = data.day_number;
  document.getElementById('res-score-display').textContent = `${data.total_score} / ${data.max_score}`;
  document.getElementById('res-pct-display').textContent = `${Math.round((data.total_score / data.max_score) * 100)}% Accuracy`;
  document.getElementById('res-time-display').textContent = formatDuration(data.time_taken_seconds || 0);

  const accordion = document.getElementById('results-questions-accordion');
  accordion.innerHTML = `
    <div class="p-6 bg-dark-850 border border-brand-500/30 rounded-2xl text-center space-y-4">
      <div class="w-16 h-16 mx-auto rounded-2xl bg-brand-500/20 text-brand-400 flex items-center justify-center text-3xl">
        <i class="fa-solid fa-circle-check"></i>
      </div>
      <div>
        <h3 class="text-xl font-bold text-white">Day ${data.day_number} Test Completed For Today!</h3>
        <p class="text-xs text-slate-400 max-w-md mx-auto mt-1">
          You have already completed today's 5 questions with a score of <strong class="text-brand-400">${data.total_score}/${data.max_score}</strong>.
          Your next daily test (Day ${data.day_number + 1}) will automatically unlock tomorrow with 5 brand new questions!
        </p>
      </div>
      <div class="pt-2 flex flex-wrap items-center justify-center gap-3">
        <button onclick="loadDailyTest(true)" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-brand-500 to-emerald-600 hover:from-brand-600 text-dark-900 font-bold text-xs shadow-lg shadow-brand-500/20 transition flex items-center space-x-2">
          <i class="fa-solid fa-unlock"></i>
          <span>Unlock Day ${data.day_number + 1} Early (Practice Ahead)</span>
        </button>
        <button onclick="showSection('progress-section')" class="px-5 py-2.5 rounded-xl bg-dark-750 hover:bg-dark-700 text-slate-300 font-semibold text-xs border border-dark-600 transition flex items-center space-x-2">
          <i class="fa-solid fa-chart-line"></i>
          <span>View Skill Roadmap</span>
        </button>
      </div>
    </div>
  `;
}

function renderQuestionPills() {
  const container = document.getElementById('question-navigator-pills');
  if (!container || !window.currentTestState) return;

  container.innerHTML = '';
  window.currentTestState.questions.forEach((q, idx) => {
    const btn = document.createElement('button');
    btn.id = `q-pill-${q.id}`;
    btn.className = `q-pill px-2.5 sm:px-3 py-1.5 rounded-xl border border-dark-700 bg-dark-800 text-xs font-semibold flex items-center space-x-1 sm:space-x-1.5 transition shrink-0 ${idx === window.currentQuestionIndex ? 'active' : ''}`;
    
    // Status
    if (window.currentTestState.question_statuses[q.id] === 'solved') {
      btn.classList.add('solved');
    }

    btn.innerHTML = `
      <span class="w-4 h-4 rounded bg-dark-700 text-slate-300 text-[10px] flex items-center justify-center font-bold font-mono">${idx + 1}</span>
      <span class="font-bold sm:hidden text-slate-200">Q${idx + 1}</span>
      <span class="hidden sm:inline truncate max-w-[100px] text-slate-300 font-medium">${q.title}</span>
    `;

    btn.onclick = () => switchQuestion(idx);
    container.appendChild(btn);
  });
}

function switchQuestion(index) {
  if (!window.currentTestState || !window.currentTestState.questions) return;
  if (index < 0 || index >= window.currentTestState.questions.length) return;

  // Save current code from editor into memory
  const prevQ = window.currentTestState.questions[window.currentQuestionIndex];
  if (prevQ && globalEditor) {
    window.currentTestState.answers[prevQ.id] = globalEditor.getValue();
  }

  window.currentQuestionIndex = index;
  const q = window.currentTestState.questions[index];

  // Update pills active state
  document.querySelectorAll('.q-pill').forEach((pill, idx) => {
    pill.classList.toggle('active', idx === index);
  });

  const counterEl = document.getElementById('current-q-pill-counter');
  if (counterEl) counterEl.textContent = index + 1;

  // On mobile screens, switch to problem view so the user reads the new question first
  if (window.innerWidth < 1024 && typeof window.setMobilePane === 'function') {
    window.setMobilePane('problem');
  }

  // Update Left Column (Problem Details)
  document.getElementById('problem-num-badge').textContent = index + 1;
  document.getElementById('problem-title').textContent = q.title;
  document.getElementById('problem-topic-badge').textContent = q.topic;
  document.getElementById('problem-diff-badge').textContent = q.difficulty;
  document.getElementById('problem-description').textContent = q.description;

  // Render Sample Test Cases Table
  const sampleContainer = document.getElementById('sample-cases-container');
  sampleContainer.innerHTML = '';
  q.sample_test_cases.forEach((tc, tcIdx) => {
    const div = document.createElement('div');
    div.className = 'p-2.5 rounded-xl bg-dark-800 border border-dark-700/80 text-xs space-y-1';
    div.innerHTML = `
      <div class="flex items-center justify-between text-[11px] text-slate-400 font-mono">
        <span class="font-bold text-slate-300">Case ${tcIdx + 1}</span>
        ${tc.explanation ? `<span class="italic text-slate-500 text-[10px]">${escapeHtml(tc.explanation)}</span>` : ''}
      </div>
      <div class="grid grid-cols-2 gap-2 text-[11px] font-mono mt-1">
        <div class="bg-dark-900/80 p-1.5 rounded text-slate-300">
          <span class="text-slate-500 text-[10px]">Input:</span> ${escapeHtml(JSON.stringify(tc.input))}
        </div>
        <div class="bg-dark-900/80 p-1.5 rounded text-emerald-400">
          <span class="text-slate-500 text-[10px]">Output:</span> ${escapeHtml(JSON.stringify(tc.expected))}
        </div>
      </div>
    `;
    sampleContainer.appendChild(div);
  });

  // Load code in Editor (saved answer or starter code)
  const initialCode = window.currentTestState.answers[q.id] || q.starter_code;
  if (globalEditor) {
    globalEditor.setValue(initialCode);
  }

  // Update Output pane to neutral prompt
  const outputContainer = document.getElementById('editor-output-container');
  const statusPill = document.getElementById('run-status-pill');
  statusPill.classList.add('hidden');
  outputContainer.innerHTML = '<div class="text-slate-500 italic">Click "Run Tests" or press Ctrl+Enter to test your Python function against sample cases.</div>';

  // Update bottom navigation buttons
  document.getElementById('current-q-index').textContent = index + 1;
  document.getElementById('prev-q-btn').disabled = (index === 0);
  document.getElementById('prev-q-btn').classList.toggle('opacity-50', index === 0);
  document.getElementById('next-q-btn').disabled = (index === window.currentTestState.questions.length - 1);
  document.getElementById('next-q-btn').classList.toggle('opacity-50', index === window.currentTestState.questions.length - 1);
}

function prevQuestion() {
  if (window.currentQuestionIndex > 0) switchQuestion(window.currentQuestionIndex - 1);
}

function nextQuestion() {
  if (window.currentTestState && window.currentQuestionIndex < window.currentTestState.questions.length - 1) {
    switchQuestion(window.currentQuestionIndex + 1);
  }
}

function resetCurrentCode() {
  const q = window.currentTestState.questions[window.currentQuestionIndex];
  if (q && confirm('Reset this question back to the original starter code?')) {
    globalEditor.setValue(q.starter_code);
    window.currentTestState.answers[q.id] = q.starter_code;
  }
}

function markPillStatus(questionId, status) {
  if (!window.currentTestState) return;
  window.currentTestState.question_statuses[questionId] = status;
  const pill = document.getElementById(`q-pill-${questionId}`);
  if (!pill) return;

  pill.classList.remove('solved');
  if (status === 'solved') {
    pill.classList.add('solved');
  }
}

// ----------------- 45-Minute Countdown Timer -----------------

function startCountdownTimer(initialSeconds) {
  if (window.timerInterval) clearInterval(window.timerInterval);

  let secondsLeft = Math.max(0, initialSeconds);
  const displayEl = document.getElementById('countdown-display');
  const barEl = document.getElementById('timer-bar');
  const iconEl = document.getElementById('timer-icon');
  const totalSeconds = 45 * 60;

  function updateDisplay() {
    displayEl.textContent = formatTime(secondsLeft);
    const pct = Math.max(0, Math.min(100, (secondsLeft / totalSeconds) * 100));
    barEl.style.width = `${pct}%`;

    // Colors: Green -> Amber -> Red
    if (secondsLeft > 10 * 60) {
      displayEl.className = 'font-mono font-bold text-lg text-brand-400 tracking-wider';
      barEl.className = 'h-full bg-brand-500 transition-all duration-1000';
      iconEl.className = 'fa-regular fa-clock text-brand-400 animate-pulse text-base';
    } else if (secondsLeft > 5 * 60) {
      displayEl.className = 'font-mono font-bold text-lg text-amber-400 tracking-wider';
      barEl.className = 'h-full bg-amber-500 transition-all duration-1000';
      iconEl.className = 'fa-regular fa-clock text-amber-400 animate-pulse text-base';
    } else {
      displayEl.className = 'font-mono font-bold text-lg text-rose-500 tracking-wider timer-critical';
      barEl.className = 'h-full bg-rose-500 transition-all duration-1000';
      iconEl.className = 'fa-regular fa-clock text-rose-500 animate-bounce text-base';
    }

    if (secondsLeft <= 0) {
      clearInterval(window.timerInterval);
      handleAutoSubmitOnExpiry();
    }
  }

  updateDisplay();

  window.timerInterval = setInterval(() => {
    secondsLeft--;
    window.currentTestState.remaining_seconds = secondsLeft;
    updateDisplay();
  }, 1000);
}

function handleAutoSubmitOnExpiry() {
  alert('⏳ Time is up! The 45-minute limit has expired. Your test is being automatically evaluated and submitted.');
  executeFinalSubmit();
}

// ----------------- Test Submission & Grading -----------------

function confirmSubmitTest() {
  const modal = document.getElementById('submit-confirm-modal');
  if (modal) modal.showModal();
}

function closeSubmitModal() {
  const modal = document.getElementById('submit-confirm-modal');
  if (modal) modal.close();
}

async function executeFinalSubmit() {
  closeSubmitModal();
  if (window.timerInterval) clearInterval(window.timerInterval);

  // Save current active question code before submitting
  const currentQ = window.currentTestState.questions[window.currentQuestionIndex];
  if (currentQ && globalEditor) {
    window.currentTestState.answers[currentQ.id] = globalEditor.getValue();
  }

  try {
    const res = await fetch('/api/test/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: window.currentTestState.session_id,
        user_id: window.currentUser.id,
        submissions: window.currentTestState.answers
      })
    });

    const report = await res.json();
    renderTestResultsSummary(report);
    showSection('results-section');

    // Confetti celebration if score is high (>= 4)
    if (report.total_score >= 4 && window.confetti) {
      window.confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });
    }

  } catch (err) {
    console.error('Submission error', err);
    alert('Submission failed due to network error.');
  }
}

// ----------------- Results Summary Rendering -----------------

function renderTestResultsSummary(report) {
  document.getElementById('result-day-num').textContent = report.day_number;
  document.getElementById('res-score-display').textContent = `${report.total_score} / ${report.max_score}`;
  document.getElementById('res-pct-display').textContent = `${report.percentage}% Accuracy`;
  document.getElementById('res-time-display').textContent = formatDuration(report.time_taken_seconds);
  document.getElementById('res-streak-display').textContent = report.new_streak;
  document.getElementById('res-level-display').textContent = getSkillLevel(report.total_score, 1);

  // Render Detailed Question Review Accordion
  const accordionContainer = document.getElementById('results-questions-accordion');
  accordionContainer.innerHTML = '';

  report.results.forEach((q, idx) => {
    const isCorrect = q.is_correct === 1;
    const card = document.createElement('div');
    card.className = `bg-dark-850 border ${isCorrect ? 'border-emerald-500/30' : 'border-rose-500/30'} rounded-2xl overflow-hidden shadow-lg`;

    card.innerHTML = `
      <!-- Accordion Header -->
      <div onclick="toggleAccordion('res-item-${idx}')" class="p-4 bg-dark-800/80 cursor-pointer flex items-center justify-between hover:bg-dark-750 transition">
        <div class="flex items-center space-x-3">
          <div class="w-7 h-7 rounded-lg ${isCorrect ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'} flex items-center justify-center font-bold font-mono text-xs">
            ${isCorrect ? '<i class="fa-solid fa-check"></i>' : '<i class="fa-solid fa-xmark"></i>'}
          </div>
          <div>
            <div class="font-bold text-sm text-white flex items-center space-x-2">
              <span>Q${idx + 1}: ${q.title}</span>
              <span class="text-[10px] px-2 py-0.5 rounded font-mono font-semibold bg-dark-700 text-slate-300">${q.topic}</span>
            </div>
            <div class="text-xs text-slate-400 mt-0.5">
              ${q.passed_cases} / ${q.total_cases} test cases passed
            </div>
          </div>
        </div>

        <div class="flex items-center space-x-3">
          <span class="text-xs font-mono font-bold px-2.5 py-1 rounded-full ${isCorrect ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'}">
            ${isCorrect ? '100% CORRECT' : 'NEEDS WORK'}
          </span>
          <i id="accordion-arrow-${idx}" class="fa-solid fa-chevron-down text-slate-400 text-xs transition-transform duration-200"></i>
        </div>
      </div>

      <!-- Accordion Content -->
      <div id="res-item-${idx}" class="p-5 border-t border-dark-700/80 space-y-4 bg-dark-850">
        <!-- Problem description -->
        <div>
          <div class="text-xs uppercase tracking-wider font-semibold text-slate-400 mb-1">Problem Objective</div>
          <p class="text-xs text-slate-300 whitespace-pre-wrap">${escapeHtml(q.description)}</p>
        </div>

        <!-- Submitted code vs Model Solution side by side -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
          <div>
            <div class="text-xs font-semibold text-slate-400 mb-1.5 flex items-center justify-between">
              <span>Your Submitted Code</span>
              <span class="text-[10px] text-slate-500 font-mono">Attempted</span>
            </div>
            <pre class="p-3 bg-dark-900 border border-dark-700 rounded-xl font-mono text-xs text-slate-200 overflow-x-auto leading-relaxed">${escapeHtml(q.user_code || '# No code submitted')}</pre>
          </div>

          <div>
            <div class="text-xs font-semibold text-emerald-400 mb-1.5 flex items-center justify-between">
              <span>Optimal Pythonic Solution</span>
              <span class="text-[10px] text-emerald-500/80 font-mono">Reference</span>
            </div>
            <pre class="p-3 bg-dark-900 border border-emerald-500/30 rounded-xl font-mono text-xs text-emerald-300 overflow-x-auto leading-relaxed">${escapeHtml(q.solution)}</pre>
          </div>
        </div>

        <!-- Explanation & Pro Tip -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
          <div class="p-3 bg-dark-800/80 rounded-xl border border-dark-700 text-xs">
            <div class="text-slate-300 font-semibold mb-1 flex items-center space-x-1.5">
              <i class="fa-solid fa-graduation-cap text-cyan-400"></i>
              <span>Concept Explanation</span>
            </div>
            <p class="text-slate-400 text-xs leading-relaxed">${escapeHtml(q.explanation)}</p>
          </div>

          <div class="p-3 bg-emerald-950/20 rounded-xl border border-emerald-500/20 text-xs">
            <div class="text-emerald-400 font-semibold mb-1 flex items-center space-x-1.5">
              <i class="fa-regular fa-lightbulb text-amber-400"></i>
              <span>Pythonic Wisdom / Tip</span>
            </div>
            <p class="text-slate-300 text-xs leading-relaxed">${escapeHtml(q.pythonic_tip)}</p>
          </div>
        </div>
      </div>
    `;

    accordionContainer.appendChild(card);
  });
}

function toggleAccordion(id) {
  const el = document.getElementById(id);
  if (el) el.classList.toggle('hidden');
}

// ----------------- Skill Progression Hub -----------------

async function loadSkillProgressHub() {
  if (!window.currentUser) return;

  try {
    const res = await fetch(`/api/user/progress?user_id=${window.currentUser.id}`);
    const data = await res.json();

    document.getElementById('hub-streak-count').textContent = data.streak;
    document.getElementById('hub-completed-count').textContent = data.total_completed_questions;
    document.getElementById('hub-total-bank').textContent = data.total_bank_questions;
    document.getElementById('hub-recommendation-text').textContent = data.recommendation;

    // Render Competency Cards Grid
    const cardsGrid = document.getElementById('skill-cards-grid');
    cardsGrid.innerHTML = '';

    data.skill_radar.forEach(skill => {
      const meta = TOPIC_METADATA[skill.topic] || {
        icon: "fa-code",
        color: "from-slate-600 to-slate-700",
        badge: "bg-slate-500/10 text-slate-400 border-slate-500/20",
        description: "Core Python concept"
      };

      const card = document.createElement('div');
      card.className = 'bg-dark-850 border border-dark-700 rounded-2xl p-4 shadow-lg flex flex-col justify-between';

      card.innerHTML = `
        <div>
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center space-x-2.5">
              <div class="w-8 h-8 rounded-xl bg-gradient-to-tr ${meta.color} text-white flex items-center justify-center text-xs shadow-md">
                <i class="fa-solid ${meta.icon}"></i>
              </div>
              <div>
                <h4 class="font-bold text-sm text-white">${skill.topic}</h4>
                <div class="text-[10px] text-slate-400">${meta.description}</div>
              </div>
            </div>
            <span class="text-xs font-mono font-bold px-2 py-0.5 rounded ${meta.badge}">
              ${skill.mastery}%
            </span>
          </div>

          <!-- Progress Bar -->
          <div class="w-full bg-dark-750 h-2 rounded-full overflow-hidden mt-3 mb-2">
            <div class="h-full bg-gradient-to-r ${meta.color} transition-all duration-500" style="width: ${skill.mastery}%"></div>
          </div>
        </div>

        <div class="flex items-center justify-between text-[11px] text-slate-500 pt-2 border-t border-dark-700/60 mt-2">
          <span>${skill.attempted} Attempted</span>
          <span>${skill.correct} Solved Completely</span>
        </div>
      `;

      cardsGrid.appendChild(card);
    });

    // Render Historical Tests
    const historyList = document.getElementById('test-history-list');
    historyList.innerHTML = '';

    if (data.test_history.length === 0) {
      historyList.innerHTML = '<div class="text-slate-500 text-xs italic py-2">No completed tests yet. Start today\'s test to record history!</div>';
    } else {
      data.test_history.forEach(sess => {
        const item = document.createElement('div');
        item.className = 'p-3 bg-dark-800 rounded-xl border border-dark-700 flex items-center justify-between text-xs';
        item.innerHTML = `
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 rounded-lg bg-brand-500/10 text-brand-400 flex items-center justify-center font-bold font-mono">
              D${sess.day_number}
            </div>
            <div>
              <div class="font-bold text-white">Daily Test #${sess.day_number}</div>
              <div class="text-[10px] text-slate-400">${new Date(sess.submitted_at || sess.started_at).toLocaleDateString()}</div>
            </div>
          </div>

          <div class="flex items-center space-x-4">
            <div class="text-right">
              <div class="font-bold text-brand-400 font-mono">${sess.total_score} / 5 Score</div>
              <div class="text-[10px] text-slate-400">${formatDuration(sess.time_taken_seconds || 0)} spent</div>
            </div>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold ${sess.total_score >= 4 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}">
              ${sess.total_score >= 4 ? 'MASTERED' : 'COMPLETED'}
            </span>
          </div>
        `;
        historyList.appendChild(item);
      });
    }

  } catch (err) {
    console.error('Failed to load progress hub', err);
  }
}

// ----------------- Mentor / Reviewer Dashboard -----------------

async function loadMentorDashboard() {
  try {
    const res = await fetch('/api/mentor/dashboard');
    const data = await res.json();

    const container = document.getElementById('mentor-students-container');
    container.innerHTML = '';

    if (data.length === 0) {
      container.innerHTML = '<div class="text-slate-500 text-xs italic">No student accounts registered yet.</div>';
      return;
    }

    data.forEach(item => {
      const student = item.student;
      const card = document.createElement('div');
      card.className = 'bg-dark-850 border border-dark-700 rounded-2xl p-6 shadow-xl space-y-6';

      let sessionsHtml = '';
      if (item.sessions.length === 0) {
        sessionsHtml = '<div class="text-slate-500 text-xs italic">No tests started yet.</div>';
      } else {
        sessionsHtml = item.sessions.map(s => `
          <div class="p-3 bg-dark-800 rounded-xl border border-dark-750 flex items-center justify-between text-xs">
            <div class="flex items-center space-x-2">
              <span class="font-bold text-brand-400 font-mono">Day ${s.day_number}</span>
              <span class="text-slate-400">Status: <strong class="${s.status === 'completed' ? 'text-emerald-400' : 'text-amber-400'}">${s.status}</strong></span>
            </div>
            <div class="flex items-center space-x-3">
              <span class="font-mono text-white font-bold">${s.total_score} / 5</span>
              <span class="text-slate-500 text-[11px]">${formatDuration(s.time_taken_seconds || 0)}</span>
            </div>
          </div>
        `).join('');
      }

      let submissionsHtml = '';
      if (item.recent_submissions.length === 0) {
        submissionsHtml = '<div class="text-slate-500 text-xs italic">No code submitted yet.</div>';
      } else {
        submissionsHtml = item.recent_submissions.map((sub, sIdx) => `
          <div class="p-3.5 bg-dark-800 rounded-xl border border-dark-750 text-xs space-y-2">
            <div class="flex items-center justify-between">
              <div class="font-bold text-white flex items-center space-x-2">
                <span>${sub.question_title}</span>
                <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-dark-700 text-slate-400">${sub.question_topic}</span>
              </div>
              <span class="font-mono text-[10px] font-bold px-2 py-0.5 rounded ${sub.is_correct ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'}">
                ${sub.passed_cases}/${sub.total_cases} Passed
              </span>
            </div>
            <div>
              <div class="text-[10px] text-slate-500 uppercase font-semibold">Friend's Written Code:</div>
              <pre class="mt-1 p-2 bg-dark-900 border border-dark-750 rounded font-mono text-[11px] text-slate-300 overflow-x-auto">${escapeHtml(sub.code)}</pre>
            </div>
            ${sub.error_message ? `<div class="text-[10px] text-rose-400 bg-rose-950/20 p-2 rounded border border-rose-900/30">${escapeHtml(sub.error_message)}</div>` : ''}
          </div>
        `).join('');
      }

      card.innerHTML = `
        <!-- Student Top Info -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-dark-700/80">
          <div class="flex items-center space-x-3">
            <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-cyan-500 to-blue-600 text-white flex items-center justify-center font-bold text-lg shadow-lg">
              ${student.name.charAt(0).toUpperCase()}
            </div>
            <div>
              <h3 class="text-lg font-bold text-white">${student.name} <span class="text-xs text-slate-400 font-mono">(@${student.username})</span></h3>
              <div class="text-xs text-slate-400 mt-0.5 flex items-center space-x-3">
                <span>Active Day: <strong class="text-brand-400 font-mono">${item.current_day}</strong></span>
                <span>Streak: <strong class="text-amber-400 font-mono">🔥 ${item.streak}</strong></span>
              </div>
            </div>
          </div>
        </div>

        <!-- Student Test Sessions Timeline -->
        <div>
          <h4 class="text-xs uppercase tracking-wider font-semibold text-slate-400 mb-2">Test Sessions History</h4>
          <div class="space-y-2">
            ${sessionsHtml}
          </div>
        </div>

        <!-- Recent Submitted Code Review -->
        <div>
          <h4 class="text-xs uppercase tracking-wider font-semibold text-slate-400 mb-2">Exact Code Submissions & Error Inspection</h4>
          <div class="space-y-3 max-h-96 overflow-y-auto pr-1">
            ${submissionsHtml}
          </div>
        </div>
      `;

      container.appendChild(card);
    });

  } catch (err) {
    console.error('Failed to load mentor dashboard', err);
  }
}

async function advanceStudentDay() {
  if (!confirm('Advance student to the Next Day? This marks today\'s session as complete and generates 5 new unseen questions.')) return;
  try {
    const res = await fetch('/api/mentor/advance-day', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: 1 })
    });
    const data = await res.json();
    alert(data.message || 'Advanced to next day!');
    loadMentorDashboard();
  } catch (e) {
    alert('Failed to advance day');
  }
}

async function resetStudentProgress() {
  if (!confirm('Reset student progress to Day 1 and clear question history? This allows taking tests completely fresh.')) return;
  try {
    const res = await fetch('/api/mentor/reset-student', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: 1 })
    });
    const data = await res.json();
    alert(data.message || 'Progress reset to Day 1.');
    loadMentorDashboard();
  } catch (e) {
    alert('Failed to reset progress');
  }
}

// ----------------- Mobile Responsive Pane Switching -----------------

function setMobilePane(pane) {
  const pProb = document.getElementById('pane-problem');
  const pEdit = document.getElementById('pane-editor');
  const pOutput = document.getElementById('pane-output');
  const editorBox = document.getElementById('editor-workspace-box');
  const tabProb = document.getElementById('mobile-tab-problem');
  const tabEdit = document.getElementById('mobile-tab-editor');
  const tabOutput = document.getElementById('mobile-tab-output');

  if (window.innerWidth >= 1024) {
    pProb?.classList.remove('hidden');
    pEdit?.classList.remove('hidden');
    pOutput?.classList.remove('hidden');
    editorBox?.classList.remove('hidden');
    return;
  }

  // Reset tab active styling
  [tabProb, tabEdit, tabOutput].forEach(t => {
    t?.classList.remove('bg-dark-700', 'text-brand-400', 'shadow-sm');
    t?.classList.add('text-slate-400');
  });

  if (pane === 'problem') {
    pProb?.classList.remove('hidden');
    pEdit?.classList.add('hidden');
    tabProb?.classList.add('bg-dark-700', 'text-brand-400', 'shadow-sm');
    tabProb?.classList.remove('text-slate-400');
  } else if (pane === 'editor') {
    pProb?.classList.add('hidden');
    pEdit?.classList.remove('hidden');
    editorBox?.classList.remove('hidden');
    pOutput?.classList.add('hidden'); // Hide output while coding on mobile to maximize typing room
    tabEdit?.classList.add('bg-dark-700', 'text-brand-400', 'shadow-sm');
    tabEdit?.classList.remove('text-slate-400');

    if (globalEditor) {
      globalEditor.updateGutter();
    }
  } else if (pane === 'output') {
    pProb?.classList.add('hidden');
    pEdit?.classList.remove('hidden');
    editorBox?.classList.add('hidden'); // Collapse editor to show test output clearly
    pOutput?.classList.remove('hidden');
    pOutput?.classList.add('h-auto', 'min-h-[300px]');
    tabOutput?.classList.add('bg-dark-700', 'text-brand-400', 'shadow-sm');
    tabOutput?.classList.remove('text-slate-400');
  }
}

window.setMobilePane = setMobilePane;

window.addEventListener('resize', () => {
  const pProb = document.getElementById('pane-problem');
  const pEdit = document.getElementById('pane-editor');
  const pOutput = document.getElementById('pane-output');
  const editorBox = document.getElementById('editor-workspace-box');
  if (window.innerWidth >= 1024) {
    pProb?.classList.remove('hidden');
    pEdit?.classList.remove('hidden');
    pOutput?.classList.remove('hidden');
    editorBox?.classList.remove('hidden');
  }
});

