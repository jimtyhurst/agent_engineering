import sys
import time
import subprocess
import json
import urllib.request
import urllib.error

PYTHON_EXEC = "/Users/jimtyhurst/src/gemini/20260725-agent-engineering/.venv/bin/python3"
PORT = 8008
BASE_URL = f"http://127.0.0.1:{PORT}"

def http_request(url, method="GET", data=None):
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            content_type = resp.headers.get("Content-Type")
            resp_body = resp.read().decode("utf-8")
            return status, json.loads(resp_body) if "application/json" in content_type else resp_body
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            parsed = json.loads(err_body)
        except Exception:
            parsed = err_body
        return e.code, parsed

def run_http_endpoint_tests():
    print(f"Starting server process on port {PORT}...")
    server = subprocess.Popen(
        [PYTHON_EXEC, "-m", "uvicorn", "app:app", "--port", str(PORT), "--host", "127.0.0.1"],
        cwd="/Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/pomodoro-timer",
        env={"PYTHONPATH": "."}
    )
    
    # Wait for server to start
    started = False
    for _ in range(20):
        time.sleep(0.2)
        try:
            with urllib.request.urlopen(f"{BASE_URL}/api/tasks") as response:
                if response.status == 200:
                    started = True
                    break
        except Exception:
            pass
            
    if not started:
        server.kill()
        sys.exit("Server failed to start")
        
    print("Server ready! Testing REST API endpoints with HTTP requests...\n")
    
    results = []

    # 1. GET /api/tasks
    status, body = http_request(f"{BASE_URL}/api/tasks", "GET")
    print(f"[GET /api/tasks] Status: {status}")
    print(f"Response: {body}\n")
    results.append(("GET /api/tasks", status == 200))

    # 2. POST /api/tasks (Success)
    new_task = {"title": "HTTP Client Test Task", "category": "Integration", "est_pomodoros": 2}
    status, body = http_request(f"{BASE_URL}/api/tasks", "POST", new_task)
    print(f"[POST /api/tasks] Status: {status}")
    print(f"Response: {body}\n")
    task_id = body.get("id") if isinstance(body, dict) else None
    results.append(("POST /api/tasks (Create)", status == 200 and task_id is not None))

    # 3. POST /api/tasks (Validation Error 400)
    invalid_task = {"title": "   ", "category": "General"}
    status, body = http_request(f"{BASE_URL}/api/tasks", "POST", invalid_task)
    print(f"[POST /api/tasks (Validation Error)] Status: {status}")
    print(f"Response: {body}\n")
    results.append(("POST /api/tasks (400 Empty Title)", status == 400))

    # 4. PUT /api/tasks/{id} (Success)
    if task_id:
        update_data = {"title": "HTTP Client Test Task (Updated)", "completed_pomodoros": 2, "status": "completed"}
        status, body = http_request(f"{BASE_URL}/api/tasks/{task_id}", "PUT", update_data)
        print(f"[PUT /api/tasks/{task_id}] Status: {status}")
        print(f"Response: {body}\n")
        results.append((f"PUT /api/tasks/{task_id}", status == 200))

    # 5. PUT /api/tasks/99999 (404 Not Found)
    status, body = http_request(f"{BASE_URL}/api/tasks/99999", "PUT", {"title": "Ghost"})
    print(f"[PUT /api/tasks/99999 (404)] Status: {status}")
    print(f"Response: {body}\n")
    results.append(("PUT /api/tasks/99999 (404)", status == 404))

    # 6. POST /api/sessions
    session_data = {"mode": "work", "duration_minutes": 25, "task_id": task_id}
    status, body = http_request(f"{BASE_URL}/api/sessions", "POST", session_data)
    print(f"[POST /api/sessions] Status: {status}")
    print(f"Response: {body}\n")
    results.append(("POST /api/sessions", status == 200))

    # 7. GET /api/stats
    status, body = http_request(f"{BASE_URL}/api/stats", "GET")
    print(f"[GET /api/stats] Status: {status}")
    print(f"Response: {body}\n")
    results.append(("GET /api/stats", status == 200))

    # 8. GET /api/settings
    status, body = http_request(f"{BASE_URL}/api/settings", "GET")
    print(f"[GET /api/settings] Status: {status}")
    print(f"Response: {body}\n")
    results.append(("GET /api/settings", status == 200))

    # 9. POST /api/settings
    settings_payload = {"settings": {"work_duration": "25", "theme": "ocean"}}
    status, body = http_request(f"{BASE_URL}/api/settings", "POST", settings_payload)
    print(f"[POST /api/settings] Status: {status}")
    print(f"Response: {body}\n")
    results.append(("POST /api/settings", status == 200))

    # 10. DELETE /api/tasks/{id} (Success)
    if task_id:
        status, body = http_request(f"{BASE_URL}/api/tasks/{task_id}", "DELETE")
        print(f"[DELETE /api/tasks/{task_id}] Status: {status}")
        print(f"Response: {body}\n")
        results.append((f"DELETE /api/tasks/{task_id}", status == 200))

    # 11. DELETE /api/tasks/99999 (404 Not Found)
    status, body = http_request(f"{BASE_URL}/api/tasks/99999", "DELETE")
    print(f"[DELETE /api/tasks/99999 (404)] Status: {status}")
    print(f"Response: {body}\n")
    results.append(("DELETE /api/tasks/99999 (404)", status == 404))

    # Clean up server
    server.terminate()
    server.wait()
    print("Server stopped cleanly.")

    print("\n--- Summary of HTTP Request Tests ---")
    all_passed = True
    for test_name, success in results:
        status_str = "PASSED" if success else "FAILED"
        if not success:
            all_passed = False
        print(f"  {test_name}: {status_str}")

    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    run_http_endpoint_tests()
