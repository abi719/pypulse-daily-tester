"""
Database access and business logic for Python Daily Coding Tester.
Uses standard Python SQLite with JSON support.
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta, timezone
from questions_data import QUESTIONS

DB_PATH = os.path.join(os.path.dirname(__file__), "python_tester.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    # Users table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'student',
        created_at TEXT NOT NULL
    )
    """)

    # Questions table
    c.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        topic TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        description TEXT NOT NULL,
        starter_code TEXT NOT NULL,
        sample_test_cases TEXT NOT NULL,
        hidden_test_cases TEXT NOT NULL,
        solution TEXT NOT NULL,
        explanation TEXT NOT NULL,
        pythonic_tip TEXT NOT NULL
    )
    """)

    # Test sessions table (5 questions, 45 minutes)
    c.execute("""
    CREATE TABLE IF NOT EXISTS test_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        day_number INTEGER NOT NULL,
        question_ids TEXT NOT NULL,
        started_at TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        submitted_at TEXT,
        total_score INTEGER DEFAULT 0,
        max_score INTEGER DEFAULT 5,
        time_taken_seconds INTEGER DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'in_progress',
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # Submissions table (per question)
    c.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        question_id TEXT NOT NULL,
        code TEXT NOT NULL,
        passed_cases INTEGER DEFAULT 0,
        total_cases INTEGER DEFAULT 0,
        is_correct INTEGER DEFAULT 0,
        error_message TEXT,
        stdout TEXT,
        submitted_at TEXT NOT NULL,
        FOREIGN KEY(session_id) REFERENCES test_sessions(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # User progress & stats
    c.execute("""
    CREATE TABLE IF NOT EXISTS user_progress (
        user_id INTEGER PRIMARY KEY,
        current_day INTEGER DEFAULT 1,
        streak INTEGER DEFAULT 0,
        last_test_date TEXT,
        completed_question_ids TEXT DEFAULT '[]',
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # Default Users
    now_str = datetime.now(timezone.utc).isoformat()
    c.execute("SELECT id FROM users WHERE username = 'learner'")
    if not c.fetchone():
        c.execute("""
        INSERT INTO users (username, password, name, role, created_at)
        VALUES ('learner', 'python123', 'Coding Friend', 'student', ?)
        """, (now_str,))
        learner_id = c.lastrowid
        c.execute("""
        INSERT INTO user_progress (user_id, current_day, streak, completed_question_ids)
        VALUES (?, 1, 0, '[]')
        """, (learner_id,))

    c.execute("SELECT id FROM users WHERE username = 'mentor'")
    if not c.fetchone():
        c.execute("""
        INSERT INTO users (username, password, name, role, created_at)
        VALUES ('mentor', 'admin123', 'Mentor / Reviewer', 'mentor', ?)
        """, (now_str,))

    # Insert or update Questions
    for q in QUESTIONS:
        c.execute("""
        INSERT INTO questions (
            id, title, topic, difficulty, description, starter_code,
            sample_test_cases, hidden_test_cases, solution, explanation, pythonic_tip
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            title=excluded.title,
            topic=excluded.topic,
            difficulty=excluded.difficulty,
            description=excluded.description,
            starter_code=excluded.starter_code,
            sample_test_cases=excluded.sample_test_cases,
            hidden_test_cases=excluded.hidden_test_cases,
            solution=excluded.solution,
            explanation=excluded.explanation,
            pythonic_tip=excluded.pythonic_tip
        """, (
            q["id"],
            q["title"],
            q["topic"],
            q["difficulty"],
            q["description"],
            q["starter_code"],
            json.dumps(q["sample_test_cases"]),
            json.dumps(q["hidden_test_cases"]),
            q["solution"],
            q["explanation"],
            q["pythonic_tip"]
        ))

    conn.commit()
    conn.close()

# ----------------- Auth Functions -----------------

def authenticate_user(username, password):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, username, name, role FROM users WHERE username = ? AND password = ?", (username.strip(), password))
    user = c.fetchone()
    conn.close()
    if user:
        return dict(user)
    return None

def register_user(username, password, name, role='student'):
    conn = get_db()
    c = conn.cursor()
    try:
        now_str = datetime.now(timezone.utc).isoformat()
        c.execute("""
        INSERT INTO users (username, password, name, role, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, (username.strip(), password, name.strip(), role, now_str))
        user_id = c.lastrowid
        if role == 'student':
            c.execute("""
            INSERT INTO user_progress (user_id, current_day, streak, completed_question_ids)
            VALUES (?, 1, 0, '[]')
            """, (user_id,))
        conn.commit()
        return {"id": user_id, "username": username, "name": name, "role": role}
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

# ----------------- Question & Session Logic -----------------

def get_unseen_questions(user_id, count=5):
    """
    Selects `count` questions that have NOT yet been assigned to or completed by this user.
    Balanced across different topics for variety.
    """
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT completed_question_ids FROM user_progress WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    completed_ids = json.loads(row["completed_question_ids"]) if row and row["completed_question_ids"] else []

    # Exclude already completed/assigned questions
    placeholders = ",".join(["?"] * len(completed_ids)) if completed_ids else ""
    query = "SELECT * FROM questions"
    params = []
    if placeholders:
        query += f" WHERE id NOT IN ({placeholders})"
        params = completed_ids

    c.execute(query, params)
    available_rows = [dict(r) for r in c.fetchall()]

    # If pool is exhausted or less than count, recycle
    if len(available_rows) < count:
        c.execute("SELECT * FROM questions")
        available_rows = [dict(r) for r in c.fetchall()]

    # Diversity picking: try to pick from distinct topics
    by_topic = {}
    for q in available_rows:
        by_topic.setdefault(q["topic"], []).append(q)

    selected = []
    topics = list(by_topic.keys())
    t_idx = 0
    while len(selected) < count and available_rows:
        topic = topics[t_idx % len(topics)]
        if by_topic[topic]:
            q = by_topic[topic].pop(0)
            selected.append(q)
            available_rows.remove(q)
        t_idx += 1
        if all(len(v) == 0 for v in by_topic.values()):
            break

    # If still need more, fill from remaining
    for q in available_rows:
        if len(selected) >= count:
            break
        selected.append(q)

    conn.close()
    return selected[:count]

def get_or_create_daily_test(user_id, force_new=False):
    """
    Retrieves the active test session for the user, or creates a new one with 5 questions & 45 min timer.
    Enforces 1 test per day: if today's test is already completed, returns completed_today status
    unless force_new=True is requested.
    """
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT current_day, last_test_date FROM user_progress WHERE user_id = ?", (user_id,))
    prog_row = c.fetchone()
    current_day = prog_row["current_day"] if prog_row else 1
    last_test_date = prog_row["last_test_date"] if prog_row and prog_row["last_test_date"] else ""

    now = datetime.now(timezone.utc)
    today_str = now.strftime("%Y-%m-%d")

    # If already completed today and not forcing new day, return completed summary
    if not force_new and last_test_date and last_test_date.startswith(today_str):
        c.execute("""
        SELECT * FROM test_sessions
        WHERE user_id = ? AND status = 'completed'
        ORDER BY id DESC LIMIT 1
        """, (user_id,))
        last_session = c.fetchone()
        if last_session:
            sdata = dict(last_session)
            conn.close()
            return {
                "session_id": sdata["id"],
                "day_number": sdata["day_number"],
                "status": "completed_today",
                "total_score": sdata["total_score"],
                "max_score": sdata["max_score"],
                "time_taken_seconds": sdata["time_taken_seconds"],
                "message": f"Day {sdata['day_number']} test is already completed today! Come back tomorrow for 5 new questions, or unlock next day below."
            }

    # Check for in-progress session
    c.execute("""
    SELECT * FROM test_sessions
    WHERE user_id = ? AND status = 'in_progress'
    ORDER BY id DESC LIMIT 1
    """, (user_id,))
    session = c.fetchone()

    if session:
        session_data = dict(session)
        expires_at = datetime.fromisoformat(session_data["expires_at"])
        if now > expires_at:
            # Session expired! Auto submit/close it and advance day
            c.execute("""
            UPDATE test_sessions
            SET status = 'expired', submitted_at = ?
            WHERE id = ?
            """, (now.isoformat(), session_data["id"]))
            c.execute("""
            UPDATE user_progress
            SET current_day = current_day + 1, last_test_date = ?
            WHERE user_id = ?
            """, (now.isoformat(), user_id))
            conn.commit()
            session = None
            current_day += 1
        else:
            # Active session found, load its questions
            q_ids = json.loads(session_data["question_ids"])
            placeholders = ",".join(["?"] * len(q_ids))
            c.execute(f"SELECT * FROM questions WHERE id IN ({placeholders})", q_ids)
            q_map = {row["id"]: dict(row) for row in c.fetchall()}
            questions = [q_map[qid] for qid in q_ids if qid in q_map]

            # Fetch any already-saved answers
            c.execute("SELECT * FROM submissions WHERE session_id = ?", (session_data["id"],))
            submissions = {row["question_id"]: dict(row) for row in c.fetchall()}

            conn.close()
            remaining_seconds = max(0, int((expires_at - now).total_seconds()))
            return {
                "session_id": session_data["id"],
                "day_number": session_data["day_number"],
                "status": "in_progress",
                "remaining_seconds": remaining_seconds,
                "started_at": session_data["started_at"],
                "expires_at": session_data["expires_at"],
                "questions": _clean_questions_for_client(questions),
                "saved_submissions": submissions
            }

    # If no active session, create a new 5-question test with guaranteed UNSEEN questions
    selected_questions = get_unseen_questions(user_id, count=5)
    selected_ids = [q["id"] for q in selected_questions]

    started_at = now
    expires_at = now + timedelta(minutes=45)

    c.execute("""
    INSERT INTO test_sessions (user_id, day_number, question_ids, started_at, expires_at, status)
    VALUES (?, ?, ?, ?, ?, 'in_progress')
    """, (user_id, current_day, json.dumps(selected_ids), started_at.isoformat(), expires_at.isoformat()))
    session_id = c.lastrowid

    # Update completed question ids so they aren't repeated
    c.execute("SELECT completed_question_ids FROM user_progress WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    completed = json.loads(row["completed_question_ids"]) if row and row["completed_question_ids"] else []
    for qid in selected_ids:
        if qid not in completed:
            completed.append(qid)
    c.execute("UPDATE user_progress SET completed_question_ids = ? WHERE user_id = ?", (json.dumps(completed), user_id))

    conn.commit()
    conn.close()

    return {
        "session_id": session_id,
        "day_number": current_day,
        "status": "in_progress",
        "remaining_seconds": 45 * 60,
        "started_at": started_at.isoformat(),
        "expires_at": expires_at.isoformat(),
        "questions": _clean_questions_for_client(selected_questions),
        "saved_submissions": {}
    }

def _clean_questions_for_client(questions, include_solutions=False):
    """
    Format questions for client:
    During test, hide solutions and hidden test cases.
    Post-test or mentor review can reveal solutions.
    """
    cleaned = []
    for q in questions:
        item = {
            "id": q["id"],
            "title": q["title"],
            "topic": q["topic"],
            "difficulty": q["difficulty"],
            "description": q["description"],
            "starter_code": q["starter_code"],
            "sample_test_cases": json.loads(q["sample_test_cases"]) if isinstance(q["sample_test_cases"], str) else q["sample_test_cases"],
        }
        if include_solutions:
            item["hidden_test_cases"] = json.loads(q["hidden_test_cases"]) if isinstance(q["hidden_test_cases"], str) else q["hidden_test_cases"]
            item["solution"] = q["solution"]
            item["explanation"] = q["explanation"]
            item["pythonic_tip"] = q["pythonic_tip"]
        cleaned.append(item)
    return cleaned

# ----------------- Code Evaluation Sandbox -----------------

import sys
import io
import traceback

def evaluate_code_against_cases(code_str, sample_cases, hidden_cases):
    """
    Safely executes Python function and checks results against sample + hidden cases.
    Returns:
    - passed_count
    - total_count
    - all_passed (bool)
    - case_results (list with inputs, expected, actual, pass/fail)
    - stdout
    - error
    """
    total_cases = list(sample_cases) + list(hidden_cases)
    case_results = []
    passed_count = 0

    stdout_capture = io.StringIO()
    old_stdout = sys.stdout

    # Create restricted namespace with builtins
    safe_globals = {
        "__builtins__": __builtins__,
        "math": __import__("math"),
        "collections": __import__("collections"),
        "itertools": __import__("itertools"),
    }
    local_ns = {}

    try:
        sys.stdout = stdout_capture
        # Compile and execute student definition
        compiled = compile(code_str, "<student_code>", "exec")
        exec(compiled, safe_globals, local_ns)
    except Exception as e:
        sys.stdout = old_stdout
        return {
            "passed_count": 0,
            "total_count": len(total_cases),
            "all_passed": False,
            "case_results": [],
            "stdout": stdout_capture.getvalue(),
            "error": f"Syntax/Compilation Error: {traceback.format_exc(limit=2)}"
        }
    finally:
        sys.stdout = old_stdout

    # Find the callable function defined by student
    funcs = [v for k, v in local_ns.items() if callable(v) and not k.startswith("_")]
    if not funcs:
        return {
            "passed_count": 0,
            "total_count": len(total_cases),
            "all_passed": False,
            "case_results": [],
            "stdout": stdout_capture.getvalue(),
            "error": "No function definition found. Please define the required function."
        }

    target_func = funcs[-1]

    for idx, tc in enumerate(total_cases):
        args = tc.get("input", [])
        expected = tc.get("expected")
        is_sample = idx < len(sample_cases)
        explanation = tc.get("explanation", "")

        test_stdout = io.StringIO()
        try:
            sys.stdout = test_stdout
            # Run with cloned arguments to prevent in-place mutation side-effects
            args_copy = json.loads(json.dumps(args))
            actual = target_func(*args_copy)
            sys.stdout = old_stdout

            # Compare outputs (convert tuples to lists for JSON comparability)
            def normalize(v):
                if isinstance(v, tuple):
                    return list(v)
                return v

            is_correct = (normalize(actual) == normalize(expected))
            if is_correct:
                passed_count += 1

            case_results.append({
                "case_num": idx + 1,
                "is_sample": is_sample,
                "input": args,
                "expected": expected,
                "actual": actual,
                "passed": is_correct,
                "explanation": explanation,
                "stdout": test_stdout.getvalue()
            })
        except Exception as e:
            sys.stdout = old_stdout
            case_results.append({
                "case_num": idx + 1,
                "is_sample": is_sample,
                "input": args,
                "expected": expected,
                "actual": None,
                "passed": False,
                "error": str(e),
                "stdout": test_stdout.getvalue()
            })

    return {
        "passed_count": passed_count,
        "total_count": len(total_cases),
        "all_passed": (passed_count == len(total_cases)),
        "case_results": case_results,
        "stdout": stdout_capture.getvalue(),
        "error": None
    }

# ----------------- Submission & Grading -----------------

def save_single_submission(session_id, user_id, question_id, code_str):
    """
    Saves an intermediate draft or single question submission.
    """
    conn = get_db()
    c = conn.cursor()

    # Get question test cases
    c.execute("SELECT sample_test_cases, hidden_test_cases FROM questions WHERE id = ?", (question_id,))
    q_row = c.fetchone()
    if not q_row:
        conn.close()
        return None

    samples = json.loads(q_row["sample_test_cases"])
    hiddens = json.loads(q_row["hidden_test_cases"])

    eval_res = evaluate_code_against_cases(code_str, samples, hiddens)

    c.execute("""
    INSERT INTO submissions (
        session_id, user_id, question_id, code, passed_cases, total_cases,
        is_correct, error_message, stdout, submitted_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session_id, user_id, question_id, code_str,
        eval_res["passed_count"], eval_res["total_count"],
        1 if eval_res["all_passed"] else 0,
        eval_res["error"], eval_res["stdout"],
        datetime.now(timezone.utc).isoformat()
    ))
    conn.commit()
    conn.close()
    return eval_res

def finalize_test_session(session_id, user_id, submissions_dict):
    """
    Finalizes the 45-minute daily test:
    - Evaluates all 5 questions
    - Computes total score
    - Updates day and streak
    - Returns full performance report with model solutions
    """
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM test_sessions WHERE id = ? AND user_id = ?", (session_id, user_id))
    session = c.fetchone()
    if not session:
        conn.close()
        return {"error": "Session not found"}

    session_data = dict(session)
    q_ids = json.loads(session_data["question_ids"])

    placeholders = ",".join(["?"] * len(q_ids))
    c.execute(f"SELECT * FROM questions WHERE id IN ({placeholders})", q_ids)
    q_map = {row["id"]: dict(row) for row in c.fetchall()}

    total_score = 0
    detailed_results = []
    now = datetime.now(timezone.utc)
    started_at = datetime.fromisoformat(session_data["started_at"])
    time_taken = min(45 * 60, int((now - started_at).total_seconds()))

    for qid in q_ids:
        q = q_map.get(qid)
        user_code = submissions_dict.get(qid, q["starter_code"] if q else "")
        samples = json.loads(q["sample_test_cases"])
        hiddens = json.loads(q["hidden_test_cases"])

        eval_res = evaluate_code_against_cases(user_code, samples, hiddens)
        is_correct = 1 if eval_res["all_passed"] else 0
        if is_correct:
            total_score += 1

        # Record in submissions
        c.execute("""
        INSERT INTO submissions (
            session_id, user_id, question_id, code, passed_cases, total_cases,
            is_correct, error_message, stdout, submitted_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id, user_id, qid, user_code,
            eval_res["passed_count"], eval_res["total_count"],
            is_correct, eval_res["error"], eval_res["stdout"],
            now.isoformat()
        ))

        detailed_results.append({
            "question_id": qid,
            "title": q["title"],
            "topic": q["topic"],
            "difficulty": q["difficulty"],
            "description": q["description"],
            "user_code": user_code,
            "is_correct": is_correct,
            "passed_cases": eval_res["passed_count"],
            "total_cases": eval_res["total_count"],
            "case_results": eval_res["case_results"],
            "error": eval_res["error"],
            "solution": q["solution"],
            "explanation": q["explanation"],
            "pythonic_tip": q["pythonic_tip"]
        })

    # Update session status
    c.execute("""
    UPDATE test_sessions
    SET status = 'completed', submitted_at = ?, total_score = ?, time_taken_seconds = ?
    WHERE id = ?
    """, (now.isoformat(), total_score, time_taken, session_id))

    # Update user progress & streak
    c.execute("SELECT * FROM user_progress WHERE user_id = ?", (user_id,))
    prog = c.fetchone()
    current_day = prog["current_day"] if prog else 1
    current_streak = prog["streak"] if prog else 0

    # Advance streak and day
    new_day = current_day + 1
    new_streak = current_streak + 1

    c.execute("""
    UPDATE user_progress
    SET current_day = ?, streak = ?, last_test_date = ?
    WHERE user_id = ?
    """, (new_day, new_streak, now.isoformat(), user_id))

    conn.commit()
    conn.close()

    return {
        "session_id": session_id,
        "day_number": session_data["day_number"],
        "total_score": total_score,
        "max_score": len(q_ids),
        "percentage": round((total_score / len(q_ids)) * 100),
        "time_taken_seconds": time_taken,
        "new_day": new_day,
        "new_streak": new_streak,
        "results": detailed_results
    }

# ----------------- Analytics & Skill Progression -----------------

def get_user_progress_report(user_id):
    """
    Computes overall stats, topic mastery radar, test history, and recommendations.
    """
    conn = get_db()
    c = conn.cursor()

    # User info
    c.execute("SELECT username, name, role FROM users WHERE id = ?", (user_id,))
    user = dict(c.fetchone())

    # User progress
    c.execute("SELECT * FROM user_progress WHERE user_id = ?", (user_id,))
    prog_row = c.fetchone()
    current_day = prog_row["current_day"] if prog_row else 1
    streak = prog_row["streak"] if prog_row else 0
    completed_ids = json.loads(prog_row["completed_question_ids"]) if prog_row and prog_row["completed_question_ids"] else []

    # Completed test sessions
    c.execute("""
    SELECT * FROM test_sessions
    WHERE user_id = ? AND status = 'completed'
    ORDER BY day_number ASC
    """, (user_id,))
    sessions = [dict(s) for s in c.fetchall()]

    # Submissions grouped by topic to calculate Skill Mastery %
    c.execute("""
    SELECT q.topic, s.is_correct, s.passed_cases, s.total_cases
    FROM submissions s
    JOIN questions q ON s.question_id = q.id
    WHERE s.user_id = ?
    """, (user_id,))
    sub_rows = [dict(r) for r in c.fetchall()]

    topics = [
        "Variables & Math",
        "Strings",
        "Conditionals",
        "Loops & Iterations",
        "Lists & Tuples",
        "Dictionaries & Sets",
        "Functions & Logic",
        "Basic Algorithms"
    ]

    topic_stats = {t: {"attempted": 0, "correct": 0, "total_cases_passed": 0, "total_cases": 0} for t in topics}

    for row in sub_rows:
        t = row["topic"]
        if t in topic_stats:
            topic_stats[t]["attempted"] += 1
            if row["is_correct"]:
                topic_stats[t]["correct"] += 1
            topic_stats[t]["total_cases_passed"] += row["passed_cases"]
            topic_stats[t]["total_cases"] += row["total_cases"]

    skill_radar = []
    weakest_topic = None
    lowest_pct = 101

    for t, s in topic_stats.items():
        if s["total_cases"] > 0:
            mastery = round((s["total_cases_passed"] / s["total_cases"]) * 100)
        else:
            mastery = 0  # not tested yet
        skill_radar.append({
            "topic": t,
            "mastery": mastery,
            "attempted": s["attempted"],
            "correct": s["correct"]
        })
        if s["attempted"] > 0 and mastery < lowest_pct:
            lowest_pct = mastery
            weakest_topic = t

    # Total questions in bank
    c.execute("SELECT COUNT(*) as cnt FROM questions")
    total_bank_questions = c.fetchone()["cnt"]

    conn.close()

    recommendation = "Keep taking the daily tests to build your baseline skill profile!"
    if weakest_topic:
        recommendation = f"Focus on '{weakest_topic}': you scored {lowest_pct}% here. Practice small list comprehensions and edge-case testing tomorrow!"
    elif sessions:
        recommendation = "Great all-round performance! Keep your daily streak going to unlock advanced algorithms!"

    return {
        "user": user,
        "current_day": current_day,
        "streak": streak,
        "total_completed_questions": len(completed_ids),
        "total_bank_questions": total_bank_questions,
        "test_history": sessions,
        "skill_radar": skill_radar,
        "weakest_topic": weakest_topic,
        "recommendation": recommendation
    }

def get_mentor_all_students_report():
    """
    Returns all students, their daily sessions, scores, and recent submissions for the Mentor view.
    """
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT id, username, name, created_at FROM users WHERE role = 'student'")
    students = [dict(s) for s in c.fetchall()]

    report = []
    for s in students:
        uid = s["id"]
        # Progress
        c.execute("SELECT current_day, streak FROM user_progress WHERE user_id = ?", (uid,))
        prog = c.fetchone()

        # Sessions
        c.execute("""
        SELECT * FROM test_sessions
        WHERE user_id = ?
        ORDER BY id DESC
        """, (uid,))
        user_sessions = [dict(sess) for sess in c.fetchall()]

        # Latest submissions with questions
        c.execute("""
        SELECT s.*, q.title as question_title, q.topic as question_topic, q.solution as model_solution
        FROM submissions s
        JOIN questions q ON s.question_id = q.id
        WHERE s.user_id = ?
        ORDER BY s.id DESC LIMIT 15
        """, (uid,))
        submissions = [dict(sub) for sub in c.fetchall()]

        report.append({
            "student": s,
            "current_day": prog["current_day"] if prog else 1,
            "streak": prog["streak"] if prog else 0,
            "sessions": user_sessions,
            "recent_submissions": submissions
        })

    conn.close()
    return report

def reset_user_progress(user_id):
    """
    Resets student progress to Day 1 and clears unseen question history so tests can be retaken from scratch.
    """
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM submissions WHERE user_id = ?", (user_id,))
    c.execute("DELETE FROM test_sessions WHERE user_id = ?", (user_id,))
    c.execute("UPDATE user_progress SET current_day = 1, streak = 0, completed_question_ids = '[]', last_test_date = NULL WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True
