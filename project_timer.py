
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

start_time = None
running_time = 0
elapsed_time = 0
paused_time = None
resume_time = 0
is_paused = False
log_file_path = " " # r"/patth/to/your/blender/file"


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
    global start_time, is_paused, elapsed_time, running_time
    running_time = 0
    elapsed_time = 0
    if start_time is None:
        start_time = time.time()
    is_paused = False
    log("Start")

def stop():
    global start_time, elapsed_time, paused_time
    if start_time is not None:
        if is_paused is not True and paused_time is not None:
            elapsed_time = time.time() - start_time - paused_time
            start_time = None
            paused_time = None
        elif is_paused is not True and paused_time is None:
            elapsed_time = time.time() - start_time
            start_time = None
        else:
            elapsed_time = paused_time
            start_time = None
    log("Stop")

def pause():
    global is_paused, elapsed_time, paused_time
    if is_paused is not True:
        is_paused = True
        elapsed_time = time.time() - start_time
        paused_time = elapsed_time
    log("Pause")

def resume():
    global is_paused, elapsed_time, paused_time
    if is_paused:
        is_paused = False
        elapsed_time = paused_time
    log("Resume")

def display_running_time():
    global start_time, is_paused, elapsed_time, paused_time, resume_time
    if start_time is not None and is_paused is not True:
        if paused_time is None:
            elapsed_time = time.time() - start_time
        elif paused_time is not None:
            resume_time = time.time()
            elapsed_time = time.time() - resume_time + paused_time

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
        else:
          layout.operator("timer.start", text="Start", icon='PLAY', emboss=True)
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