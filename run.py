import uvicorn
import sys
import os

if __name__ == "__main__":
    print("Starting AI Financial Analyst & Report Generator...")
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
