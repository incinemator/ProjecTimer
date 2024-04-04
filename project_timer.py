import bpy
import time
import threading

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
        # Refresh the timer
        #elapsed_time = 0

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

# Function to monitor Blender window focus
def monitor_window_focus():
    global is_paused
    while True:
        try:
            if bpy.context.window_manager.windows[0].fullscreen:
                resume_timer()
            else:
                pause_timer()
        except:
            pass
        time.sleep(1)

# Event handler for when Blender is closed or another file loaded
def on_blender_exit(dummy):
    stop_timer()
    elapsed_time = 0

# Event handler when Blender regains focus
def on_blender_focus(dummy):
    resume_timer()

# UI
class PT_ProjectTimer(bpy.types.Panel):
    bl_label = "Project Timer"
    bl_idname = "panel.project_timer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Timer'

    def draw(self, context):
        layout = self.layout
        global elapsed_time

        # Display elapsed time
        layout.label(text="Time Spent: %.2f seconds" % elapsed_time)

        # Buttons
        layout.operator("timer.start", text="Start")
        layout.operator("timer.pause", text="Pause")
        row = layout.row()
        row.operator("timer.stop", text="Stop")
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
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
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
    bpy.app.handlers.load_post.append(on_blender_exit)
    threading.Thread(target=monitor_window_focus, daemon=True).start()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.app.handlers.load_post.remove(on_blender_exit)

if __name__ == "__main__":
    register()