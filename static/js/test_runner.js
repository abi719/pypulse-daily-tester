/**
 * Test Execution Runner
 * Evaluates Python code against test cases and renders output tables.
 */

async function runSampleTestCases() {
  if (!window.currentTestState || !window.currentTestState.questions) return;
  const q = window.currentTestState.questions[window.currentQuestionIndex];
  if (!q) return;

  const code = globalEditor.getValue();
  const runBtn = document.getElementById('run-cases-btn');
  const outputContainer = document.getElementById('editor-output-container');
  const statusPill = document.getElementById('run-status-pill');

  // Loading state
  runBtn.disabled = true;
  runBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin text-[10px]"></i><span>Running...</span>';
  outputContainer.innerHTML = '<div class="text-slate-400 italic flex items-center space-x-2"><i class="fa-solid fa-circle-notch fa-spin text-brand-400"></i><span>Executing Python test cases...</span></div>';
  statusPill.classList.add('hidden');

  try {
    const res = await fetch('/api/test/run-sample', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question_id: q.id, code: code })
    });

    const data = await res.json();
    runBtn.disabled = false;
    runBtn.innerHTML = '<i class="fa-solid fa-play text-[10px]"></i><span>Run Tests</span>';

    // Save draft code in state
    window.currentTestState.answers[q.id] = code;

    // Render results
    renderTestResults(data, outputContainer, statusPill, q.id);

  } catch (err) {
    runBtn.disabled = false;
    runBtn.innerHTML = '<i class="fa-solid fa-play text-[10px]"></i><span>Run Tests</span>';
    outputContainer.innerHTML = `<div class="text-rose-400 font-mono text-xs">Network/Execution Error: ${err.message}</div>`;
  }
}

function renderTestResults(data, container, statusPill, questionId) {
  if (data.error) {
    statusPill.className = "text-[10px] font-mono px-2 py-0.5 rounded font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30";
    statusPill.textContent = "Error";
    statusPill.classList.remove('hidden');

    container.innerHTML = `
      <div class="p-3 bg-rose-950/40 border border-rose-800/60 rounded-xl space-y-2">
        <div class="text-rose-400 font-bold flex items-center space-x-1.5">
          <i class="fa-solid fa-circle-xmark"></i>
          <span>Execution Failure</span>
        </div>
        <pre class="output-log text-[11px] text-rose-300 font-mono">${escapeHtml(data.error)}</pre>
      </div>
    `;
    markPillStatus(questionId, 'error');
    return;
  }

  // Render cases
  const allPassed = data.all_passed;
  statusPill.classList.remove('hidden');

  if (allPassed) {
    statusPill.className = "text-[10px] font-mono px-2 py-0.5 rounded font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30";
    statusPill.textContent = `${data.passed_count}/${data.total_count} Passed`;
    markPillStatus(questionId, 'solved');
  } else {
    statusPill.className = "text-[10px] font-mono px-2 py-0.5 rounded font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30";
    statusPill.textContent = `${data.passed_count}/${data.total_count} Passed`;
    markPillStatus(questionId, 'partial');
  }

  let html = `<div class="space-y-2">`;

  // Standard output if any
  if (data.stdout && data.stdout.trim()) {
    html += `
      <div class="p-2 bg-dark-800 rounded-lg border border-dark-700 text-xs">
        <span class="text-slate-400 font-semibold uppercase text-[10px] tracking-wider">Console Output:</span>
        <pre class="mt-1 text-slate-200 text-[11px] font-mono">${escapeHtml(data.stdout)}</pre>
      </div>
    `;
  }

  // Cases breakdown
  data.case_results.forEach((tc) => {
    const isPassed = tc.passed;
    const badgeColor = isPassed ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" : "bg-rose-500/20 text-rose-400 border-rose-500/30";
    const statusIcon = isPassed ? '<i class="fa-solid fa-check text-emerald-400"></i>' : '<i class="fa-solid fa-xmark text-rose-400"></i>';

    html += `
      <div class="p-2.5 rounded-xl bg-dark-800 border ${isPassed ? 'border-emerald-500/20' : 'border-rose-500/30'}">
        <div class="flex items-center justify-between mb-1.5">
          <div class="flex items-center space-x-2">
            ${statusIcon}
            <span class="font-bold text-xs ${isPassed ? 'text-emerald-300' : 'text-rose-300'}">Sample Case ${tc.case_num}</span>
          </div>
          <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded ${badgeColor}">
            ${isPassed ? 'PASSED' : 'FAILED'}
          </span>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] font-mono mt-1">
          <div class="bg-dark-900/60 p-1.5 rounded">
            <span class="text-slate-500 text-[10px]">Input: </span>
            <span class="text-slate-200">${escapeHtml(JSON.stringify(tc.input))}</span>
          </div>
          <div class="bg-dark-900/60 p-1.5 rounded">
            <span class="text-slate-500 text-[10px]">Expected: </span>
            <span class="text-emerald-400">${escapeHtml(JSON.stringify(tc.expected))}</span>
          </div>
        </div>
        ${!isPassed ? `
          <div class="mt-1.5 bg-rose-950/30 p-1.5 rounded border border-rose-900/40 text-[11px] font-mono">
            <span class="text-rose-400 text-[10px]">Actual Output: </span>
            <span class="text-rose-200">${escapeHtml(JSON.stringify(tc.actual))}</span>
            ${tc.error ? `<div class="text-rose-400 text-[10px] mt-0.5">${escapeHtml(tc.error)}</div>` : ''}
          </div>
        ` : ''}
      </div>
    `;
  });

  html += `</div>`;
  container.innerHTML = html;
}

function escapeHtml(str) {
  if (typeof str !== 'string') str = String(str);
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

window.runSampleTestCases = runSampleTestCases;
