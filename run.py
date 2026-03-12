# Implementation: AI generated

"""
Startup script for production deployment.
Sets up Python path so backend modules can find each other,
then launches uvicorn.
"""
import os
import sys
import uvicorn

backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
sys.path.insert(0, backend_dir)

port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port)
