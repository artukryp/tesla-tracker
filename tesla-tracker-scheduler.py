import subprocess
import time
from datetime import datetime
from config import SCRIPT_PATH


INTERVAL_MINUTES = 15
START_HOUR = 0
END_HOUR = 7

def should_execute():
    current_hour = datetime.now().hour
    return START_HOUR <= current_hour < END_HOUR

def ejecutar_script():
    print(f"🕒 Ejecutando Tesla-Tracker: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        subprocess.run(["python3", SCRIPT_PATH], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar el script: {e}")

def main():
    while True:
        if should_execute():
            ejecutar_script()
        time.sleep(INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    main()