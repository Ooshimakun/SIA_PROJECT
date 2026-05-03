import subprocess
import time
import sys

print("Booting up Enterprise Systems...")

# Launch all three APIs in the background
# Because we run this from an activated terminal, they inherit the .venv!
processes = [
    subprocess.Popen([sys.executable, "backend/catalog_api.py"]),
    subprocess.Popen([sys.executable, "backend/notification_api.py"]),
    subprocess.Popen([sys.executable, "backend/borrowing_api.py"])
]

try:
    print("=========================================")
    print(" All systems are running in the background!")
    print(" Press CTRL+C to shut them all down.")
    print("=========================================\n")
    
    # Keep the main script alive so the background processes stay running
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nShutting down Enterprise Systems...")
    # Cleanly kill all APIs when you press Ctrl+C
    for p in processes:
        p.terminate()
    print("All systems safely offline.")