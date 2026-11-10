import uvicorn
import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    print("=" * 65)
    print("  AyurRAG Backend: Cross-Textual Ayurvedic Knowledge Retrieval")
    print("  CMR College of Engineering & Technology - CSE Dept")
    print("=" * 65)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
