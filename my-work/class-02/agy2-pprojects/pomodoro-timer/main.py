import uvicorn
import os
import sys

def main():
    port = int(os.getenv("PORT", 8000))
    print(f"Starting ZenFlow Pomodoro Server on http://127.0.0.1:{port}")
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)

if __name__ == "__main__":
    main()
