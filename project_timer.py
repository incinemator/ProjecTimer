
bl_info = {
    "name": "ProjecTimer",
    "author": "Giorgos Giannakoudakis",
    "version": (1, 1),
    "blender": (4, 1, 0),
    "description": "Timer panel to track the time spent on a project ",
    "category": "Productivity",
}

import bpy
import time
import os

# Global variables for time tracking
# Custom attributes have been tried but they proved
# to be less practical for this application.

start_time = 0.0
pause_time = 0.0
resume_time = 0.0
stop_time = 0.0
running_time = 0.0
elapsed_time = 0.0
dt = 0.0 # Time interval from start/resume to pause/stop
is_paused = False
is_stopped = False
log_file_path =r"D:/Blender Projects/ProjecTimer"


#============================ Timer Functions ============================ 

# Automatic path setting
def set_log_file_path(dummy):
    global log_file_path
    blend_file_path = bpy.data.filepath
    if blend_file_path:
        log_file_path = os.path.splitext(blend_file_path)[0] + "_timer_log.txt"
        print("Log file path set to: ", log_file_path)
    else:
        print("Blend file not saved yet")

# Set the log file path when the project is loaded


def start():
    global start_time, resume_time, is_paused, elapsed_time, running_time
    running_time = 0.0
    elapsed_time = 0.0
    if start_time is 0.0:
        start_time = time.time()
        resume_time = start_time
    is_paused = False
    log("Start")

def stop():
    global start_time, stop_time, resume_time, elapsed_time, pause_time, dt, is_stopped
    elapsed_time = 0.0
    is_stopped = True
    stop_time = time.time()
    if start_time is not 0.0:
        if is_paused is not True and pause_time is not 0.0:
            dt = stop_time - resume_time
            elapsed_time += dt
            start_time = 0.0
            pause_time = 0.0
        else:
            dt = stop_time - pause_time
            elapsed_time += dt
            start_time = 0.0
            pause_time = 0.0
    log("Stop")

def pause():
    global is_paused, elapsed_time, pause_time, dt
    if is_paused is not True:
        is_paused = True
        pause_time = time.time()
        dt = pause_time - resume_time
        elapsed_time += dt
    log("Pause")

def resume():
    global is_paused, elapsed_time, pause_time, resume_time
    if is_paused:
        resume_time = time.time()
        is_paused = False
    else:
        pass
    log("Resume")

def display_running_time():
    global elapsed_time
    return elapsed_time


# Format time into HH:MM:SS
def format_time(seconds):
    seconds = int(seconds % 60)
    minutes = int((seconds % 3600)//60)
    hours = int(seconds//3600)
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

def log(message):
    global log_file_path
    with open(log_file_path, "a") as log_file:
        log_file.write("{}: {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), message))

#========================================================================

# Check if the file has been saved
def is_file_saved():
    return bool(bpy.data.filepath)


# UI
class PT_ProjectTimer(bpy.types.Panel):
    bl_label = "ProjecTimer"
    bl_idname = "panel.project_timer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Timer'

    def draw(self, context):
        layout = self.layout
        global elapsed_time, running_time
        box = layout.box()

        # Display elapsed time
        box.label(text="Time Spent: {}".format(format_time(elapsed_time)), icon='PREVIEW_RANGE')
        # Buttons
        if is_file_saved():
            layout.operator("timer.start", text="Start", icon='PLAY')
            # Alternatively:
            # layout.operator("timer.start", text="Start", icon='PLAY', emboss=False).enabled=True
        else:
          layout.operator("timer.start", text="Start", icon='PLAY', emboss=True)
          # Alternatively:
          # layout.operator("timer.start", text="Start", icon='PLAY', emboss=True).enabled=False
        layout.operator("timer.pause", text="Pause", icon='PAUSE')
        row = layout.row()
        row.operator("timer.resume", text="Resume", icon='RECOVER_LAST')
        row.operator("timer.stop", text="Stop", icon='SNAP_FACE')
        layout.operator("timer.display_current_time", text="Display Elapsed Time")

# Operator to start the timer
class StartTimerOperator(bpy.types.Operator):
    bl_idname = "timer.start"
    bl_label = "Start Timer"

    def execute(self, context):
        start()
        return {'FINISHED'}
    
# Operator to stop the timer
class StopTimerOperator(bpy.types.Operator):
    bl_idname = "timer.stop"
    bl_label = "Stop Timer"

    def execute(self, context):
        stop()
        return {'FINISHED'}
    
# Operator to pause the timer
class PauseTimerOperator(bpy.types.Operator):
    bl_idname = "timer.pause"
    bl_label = "Pause Timer"

    def execute(self, context):
        pause()
        return {'FINISHED'}
    
# Operator to resume the timer
class ResumeTimerOperator(bpy.types.Operator):
    bl_idname = "timer.resume"
    bl_label = "Resume Timer"

    def execute(self, context):
        resume()
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
    #set_log_file_path(None)
    bpy.app.handlers.load_post.append(set_log_file_path)
    bpy.app.handlers.save_post.append(set_log_file_path)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.app.handlers.load_post.append(set_log_file_path)
    bpy.app.handlers.save_post.append(set_log_file_path)

if __name__ == "__main__":
    register()