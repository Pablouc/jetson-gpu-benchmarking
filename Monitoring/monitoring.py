from execution_manager import lock, current_apps, executing
import time
import threading


def monitor_current_apps(interval=1):
    global current_apps

    while executing:
        with lock:
            print(f"Currently executing apps: {', '.join(current_apps)}")
        time.sleep(interval)