import time
import subprocess
import os

if __name__ == "__main__":
    proc = subprocess.Popen("mosquitto -p 8000", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
    while proc.poll() is None:
        time.sleep(2)
        print("ALIVE")
    print("DEAD")