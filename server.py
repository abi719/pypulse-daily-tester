"""
Lightweight, zero-external-dependency HTTP & REST API server for Python Daily Tester.
Uses Python standard library http.server with ThreadingHTTPServer.
"""

import http.server
import json
import os
import sys
import urllib.parse
from datetime import datetime

import database

PORT = int(os.environ.get("PORT", 8080))
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

class PythonTesterHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def _read_json(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            return json.loads(body)
        except Exception:
            return {}

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # API Routes
        if path == "/api/test/today":
            user_id = int(query.get("user_id", [1])[0])
            force_new = query.get("force_new", ["false"])[0].lower() == "true"
            test_data = database.get_or_create_daily_test(user_id, force_new=force_new)
            self._send_json(test_data)
            return

        elif path == "/api/user/progress":
            user_id = int(query.get("user_id", [1])[0])
            report = database.get_user_progress_report(user_id)
            self._send_json(report)
            return

        elif path == "/api/mentor/dashboard":
            mentor_data = database.get_mentor_all_students_report()
            self._send_json(mentor_data)
            return

        elif path == "/api/questions/bank":
            conn = database.get_db()
            c = conn.cursor()
            c.execute("SELECT id, title, topic, difficulty, description FROM questions")
            questions = [dict(r) for r in c.fetchall()]
            conn.close()
            self._send_json({"questions": questions})
            return

        # Default static file serving
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        data = self._read_json()

        if path == "/api/auth/login":
            username = data.get("username", "")
            password = data.get("password", "")
            user = database.authenticate_user(username, password)
            if user:
                self._send_json({"success": True, "user": user})
            else:
                self._send_json({"success": False, "message": "Invalid username or password."}, status=401)
            return

        elif path == "/api/auth/register":
            username = data.get("username", "")
            password = data.get("password", "")
            name = data.get("name", username)
            role = data.get("role", "student")
            if not username or not password:
                self._send_json({"success": False, "message": "Username and password required."}, status=400)
                return
            new_user = database.register_user(username, password, name, role)
            if new_user:
                self._send_json({"success": True, "user": new_user})
            else:
                self._send_json({"success": False, "message": "Username already exists."}, status=400)
            return

        elif path == "/api/test/run-sample":
            question_id = data.get("question_id")
            code_str = data.get("code", "")
            conn = database.get_db()
            c = conn.cursor()
            c.execute("SELECT sample_test_cases FROM questions WHERE id = ?", (question_id,))
            q_row = c.fetchone()
            conn.close()
            if not q_row:
                self._send_json({"error": "Question not found"}, status=404)
                return
            samples = json.loads(q_row["sample_test_cases"])
            eval_res = database.evaluate_code_against_cases(code_str, samples, [])
            self._send_json(eval_res)
            return

        elif path == "/api/test/save-draft":
            session_id = data.get("session_id")
            user_id = data.get("user_id")
            question_id = data.get("question_id")
            code_str = data.get("code", "")
            eval_res = database.save_single_submission(session_id, user_id, question_id, code_str)
            self._send_json({"saved": True, "evaluation": eval_res})
            return

        elif path == "/api/test/submit":
            session_id = data.get("session_id")
            user_id = data.get("user_id")
            submissions_dict = data.get("submissions", {})
            res = database.finalize_test_session(session_id, user_id, submissions_dict)
            self._send_json(res)
            return

        elif path == "/api/mentor/reset-student":
            user_id = data.get("user_id", 1)
            database.reset_user_progress(user_id)
            self._send_json({"success": True, "message": "Student progress reset to Day 1."})
            return

        elif path == "/api/mentor/advance-day":
            user_id = data.get("user_id", 1)
            conn = database.get_db()
            c = conn.cursor()
            c.execute("UPDATE test_sessions SET status = 'completed' WHERE user_id = ? AND status = 'in_progress'", (user_id,))
            c.execute("UPDATE user_progress SET current_day = current_day + 1 WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()
            self._send_json({"success": True, "message": "Advanced to next day."})
            return

        self._send_json({"error": "Not Found"}, status=404)

def run_server():
    database.init_db()
    server_address = ("", PORT)
    httpd = http.server.ThreadingHTTPServer(server_address, PythonTesterHandler)
    print(f">> Python Daily Tester running at: http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
