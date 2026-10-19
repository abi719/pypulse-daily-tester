# PyPulse Daily | 5-Question 45-Minute Python Test Platform

A modern, distraction-free platform designed to test and level up Python coding fundamentals every day.

---

## 🌟 Key Features

1. **5 Questions Per Day (No Repeats)**:
   - Intelligent question selector draws 5 unseen questions from a curriculum bank of 30+ categorized problems (Variables & Math, Strings, Conditionals, Loops, Lists, Dictionaries, Functions, and Basic Algorithms).
   - Once a question is assigned or completed, it will never repeat on future days until the entire bank has been cycled.

2. **Strict 45-Minute Countdown Timer**:
   - Real-time countdown clock in the top banner with visual progress bar.
   - Smooth color transitions (Emerald -> Amber at 10m -> Pulsing Red at 5m).
   - If the timer hits zero (`00:00`), the test is automatically submitted and graded!
   - Timer and code are persisted so accidental browser refreshes do not lose progress.

3. **In-Browser Code Editor & Safe Execution Sandbox**:
   - Monospace editor with line numbers, 4-space tab handling, auto-closing brackets/quotes, and `Ctrl+Enter` shortcut.
   - Live **Run Tests** runner that evaluates solutions against sample test cases and displays inputs, expected vs actual outputs, pass/fail status, and console print logs.

4. **Post-Test Score & Solution Review**:
   - Immediate score report (e.g., `5/5 (100% Accuracy)`), time spent, and streak count.
   - Question-by-question breakdown with the student's submitted code side-by-side with the **Optimal Pythonic Solution**.
   - Step-by-step concept explanations and "Pythonic Pro-Tips".

5. **Skill Progression Hub**:
   - Tracks mastery across 8 foundational Python domains:
     - Variables & Math
     - String Manipulation & Slicing
     - Conditionals & Branching
     - Loops & Iterations
     - Lists & Tuples
     - Dictionaries & Sets
     - Functions & Logic
     - Basic Algorithms
   - Daily streak tracking (`🔥 Day Streak`) and personalized practice recommendations based on weaker topics.

6. **Mentor / Reviewer Dashboard (For You)**:
   - Review your friend's performance across all completed days.
   - Inspect their exact code submissions, error tracebacks, and test cases passed.
   - One-click buttons to advance the student to the next day or reset question history for fresh practice.

---

## 🔑 Login Credentials

The platform includes convenient 1-click fast login buttons right on the sign-in screen, or you can enter:

| Role | Username | Password | Purpose |
| :--- | :--- | :--- | :--- |
| **Friend / Student** | `learner` | `python123` | Takes the daily 5-question 45-minute challenge, sees their score & skill roadmap |
| **Mentor / Admin** | `mentor` | `admin123` | Inspects student progress, reviews exact submitted code, tracks scores & streaks |

You can also create custom accounts using the **"Create an account"** option.

---

## 🚀 How to Run

1. Open a terminal or PowerShell in this directory:
   ```powershell
   cd C:\Users\R.Abirami\.gemini\antigravity\scratch\python-daily-tester
   ```

2. Start the Python server (no external pip dependencies required — uses Python's built-in standard library):
   ```powershell
   python server.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:8080
   ```

---

## 📁 Project Structure

```
python-daily-tester/
├── server.py              # Zero-dependency Python HTTP & REST API server
├── database.py            # SQLite database with session & grading logic
├── questions_data.py      # Curated bank of 30+ basic-to-intermediate Python problems
├── python_tester.db       # Auto-created SQLite database file
├── README.md              # Project documentation
└── static/
    ├── index.html         # Main responsive web interface
    ├── css/
    │   └── style.css      # Dark cyber theme, animations, editor typography
    └── js/
        ├── app.js         # Core application workflow, timer, auth, views
        ├── editor.js      # Code editor with line numbers & indentation
        ├── test_runner.js # Test case execution & result display
        └── data.js        # Topic metadata & formatters
```
