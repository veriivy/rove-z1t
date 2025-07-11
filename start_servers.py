import subprocess
import sys
import time
import os

def start_python_backend():
    """Start the Python Flask backend server"""
    print("🚀 Starting Python backend server...")
    try:
        # Install requirements if needed
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        
        # Start the Flask server
        subprocess.Popen([sys.executable, "python_backend.py"])
        print("✅ Python backend started on http://localhost:5000")
        return True
    except Exception as e:
        print(f"❌ Failed to start Python backend: {e}")
        return False

def start_nextjs_frontend():
    """Start the Next.js frontend server"""
    print("🚀 Starting Next.js frontend server...")
    try:
        # Navigate to the flight-recommendation-tool directory
        os.chdir("flight-recommendation-tool")
        
        # Install dependencies if needed
        subprocess.run(["npm", "install"], check=True)
        
        # Start the Next.js development server
        subprocess.Popen(["npm", "run", "dev"])
        print("✅ Next.js frontend started on http://localhost:3000")
        return True
    except Exception as e:
        print(f"❌ Failed to start Next.js frontend: {e}")
        return False

def main():
    print("🎯 Starting Flight Recommendation Tool...")
    print("This will start both the Python backend and Next.js frontend.")
    print()
    
    # Start Python backend
    if not start_python_backend():
        print("❌ Could not start Python backend. Exiting.")
        return
    
    # Wait a moment for Python backend to start
    time.sleep(2)
    
    # Start Next.js frontend
    if not start_nextjs_frontend():
        print("❌ Could not start Next.js frontend. Exiting.")
        return
    
    print()
    print("🎉 Both servers are starting up!")
    print("📱 Frontend: http://localhost:3000")
    print("🐍 Backend: http://localhost:5000")
    print()
    print("The Next.js app will now use your actual Python code!")
    print("Press Ctrl+C to stop both servers.")

if __name__ == "__main__":
    main() 