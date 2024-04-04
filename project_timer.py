import bpy
import time

# Global variables for time tracking
start_time = None
elapsed_time = 0
is_paused = False

# Start the timer
def start_timer():
    global start_time, is_paused
    start_time = time.time()
    is_paused = False
