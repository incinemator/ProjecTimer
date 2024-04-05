
bl_info = {
    "name": "ProjecTimer",
    "author": "Giorgos Giannakoudakis",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "description": "Timer panel to track the time spent on a project ",
    "category": "Productivity",
}

import bpy
import time
import threading

# Global variables for time tracking
start_time = None
running_time = 0
elapsed_time = 0
is_paused = False

# Start the timer
def start_timer():
    global start_time, is_paused, running_time, elapsed_time
    elapsed_time = 0
    if start_time is None:
        start_time = time.time() - running_time
    is_paused = False

# Stop the timer
def stop_timer():
    global start_time, elapsed_time, running_time
    if start_time is not None:
        elapsed_time = time.time() - start_time
        start_time = None
        running_time = 0

# Pause the timer
def pause_timer():
    global is_paused
    if is_paused is not True:
        is_paused = True
        running_time = time.time() - start_time

# Resume the timer
def resume_timer():
    global start_time, is_paused
    if is_paused:
        start_time = time.time() - elapsed_time
        is_paused = False

def display_running_time():
    global start_time, running_time
    if start_time is not None:
        running_time = time.time() - start_time

# UI
class PT_ProjectTimer(bpy.types.Panel):
    bl_label = "Project Timer"
    bl_idname = "panel.project_timer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Timer'

    def draw(self, context):
        layout = self.layout
        global elapsed_time, running_time

        # Display elapsed time
        layout.label(text="Time Spent: %.2f seconds" % elapsed_time)

        # Buttons
        layout.operator("timer.start", text="Start", icon='PLAY')
        layout.operator("timer.pause", text="Pause", icon='PAUSE')
        row = layout.row()
        row.operator("timer.stop", text="Stop", icon='SNAP_FACE')
        row.operator("timer.resume", text="Resume")
        layout.operator("timer.display_current_time", text="Display Elapsed Time")

# Operator to start the timer
class StartTimerOperator(bpy.types.Operator):
    bl_idname = "timer.start"
    bl_label = "Start Timer"

    def execute(self, context):
        start_timer()
        return {'FINISHED'}
    
# Operator to stop the timer
class StopTimerOperator(bpy.types.Operator):
    bl_idname = "timer.stop"
    bl_label = "Stop Timer"

    def execute(self, context):
        stop_timer()
        return {'FINISHED'}
    
# Operator to pause the timer
class PauseTimerOperator(bpy.types.Operator):
    bl_idname = "timer.pause"
    bl_label = "Pause Timer"

    def execute(self, context):
        pause_timer()
        return {'FINISHED'}
    
# Operator to resume the timer
class ResumeTimerOperator(bpy.types.Operator):
    bl_idname = "timer.resume"
    bl_label = "Resume Timer"

    def execute(self, context):
        resume_timer()
        return {'FINISHED'}
    
class DisplayCurrentTimeOperator(bpy.types.Operator):
    bl_idname = "timer.display_current_time"
    bl_label = "Display Current Time"

    def execute(self, context):
        display_running_time()
        return {'FINISHED'}

# Register classes
classes = (
    PT_ProjectTimer,
    StartTimerOperator,
    StopTimerOperator,
    PauseTimerOperator,
    ResumeTimerOperator,
    DisplayCurrentTimeOperator
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()