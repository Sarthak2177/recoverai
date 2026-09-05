"""
RecoverAI Demo Runner
"""
import os
import subprocess
import time
import sys

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(root_dir, "data")
    if not os.path.exists(os.path.join(data_dir, "transactions.json")):
        print("Generating synthetic data...")
        subprocess.run([sys.executable, os.path.join(data_dir, "generate_synthetic.py")], check=True)
    
    print("\n🚀 Starting RecoverAI Demo Environment...")
    print("🌐 Starting FastAPI Server on http://localhost:8000")
    print("   Press Ctrl+C to stop.\n")
    
    import uvicorn
    uvicorn.run("server.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
