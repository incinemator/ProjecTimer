
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

class Timer:
    def __init__(self):
        self.start_time = None
        self.running_time = 0
        self.elapsed_time = 0
        self.paused_time = 0
        self.resume_time = 0
        self.is_paused = False

    # Start the timer
    def start_timer(self):
        if self.start_timer is None:
            self.start_time = time.time()
        self.is_paused = False

    # Stop the timer
    def stop_tmer(self):
        if self.start_time is not None:
            if self.is_paused is not True and self.paused_time is not None:
                self.elapsed_time = time.time() - self.start_time - self.paused_time
                self.start_time = None
                self.paused_time = None
        elif self.is_paused is not True and self.paused_time is None:
            self.elapsed_time = time.time() - self.start_time
            self.start_time = None
        else:
            self.elapsed_time = self.paused_time
            self.start_time = None

    # Pause the timer
    def pause_timer(self):
        if self.is_paused is not True:
            self.is_paused = True
            self.elapsed_time = time.time() - self.start_time
            self.paused_time = self.elapsed_time

    # Resume the timer
    def resume_timer(self):
        if self.is_paused:
            self.is_paused = False
            self.elapsed_time = self.paused_time

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

        # Display elapsed time
        #layout.label(text="Running Time: %.2f seconds" % running_time)
        layout.label(text="Time Spent: {}".format(format_time(elapsed_time)))

        # Buttons
        layout.operator("timer.start", text="Start", icon='PLAY')
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