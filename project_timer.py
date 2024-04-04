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

# Stop the timer
def stop_timer():
    global start_time, elapsed_time
    if start_time is not None:
        elapsed_time += time.time() - start_time
        start_time = None

# Pause the timer
def pause_timer():
    global is_paused
    is_paused = True

# Resume the timer
def resume_timer():
    global start_time, is_paused
    if is_paused:
        start_time = time.time()
        is_paused = False

# Event handler for when Blender is closed or another file loaded
def on_blender_exit(dummy):
    stop_timer()

# Event handler when Blender regains focus
def on_blender_focus(dummy):
    resume_timer()

# UI
class PT_ProjectTimer(bpy.types.Panel):
    bl_label = "Project Timer"
    bl_idname = "panel.project_timer"
    bl_space_type = 'VIEW_3D'
    bl_region_tye = 'UI'
    bl_category = 'Timer'

    def draw(self, context):
        layout = self.layout
        global elapsed_time

        # Display elapsed time
        layout.label(text="Time Spent: %.2f seconds" % elapsed_time)

        # Buttons
        row = layout.row()
        row.operator("timer.start", text="Start")
        row.operator("timer.stop", text="Stop")
        row.operator("timer.pause", text="Pause")
        row.operator("timer.resume", text="Resume")