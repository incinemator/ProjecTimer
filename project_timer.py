
bl_info = {
    "name": "ProjecTimer",
    "author": "Giorgos Giannakoudakis",
    "version": (1, 2),
    "blender": (4, 1, 0),
    "description": "Timer panel to track the time spent on a project ",
    "category": "Productivity",
}

import bpy
import time

# Global variables for time tracking
# Custom attributes have been tried but they proved
# to be less practical for this application.

start_time = None
running_time = 0
elapsed_time = 0
paused_time = 0
resume_time = 0
is_running = True
log_file_path = r"/path/to/your/project.txt"


# Start the timer
def start():
    global is_running, start_time
    if is_running:
        start_time = time.time()
        log("Start")

# Stop the timer
def stop():
    global is_running, elapsed_time, start_time, paused_time, is_running
    if is_running:
        elapsed_time += time.time() - start_time
        start_time = 0
        paused_time = 0
        is_running = False
        log("Stop")


# Pause the timer
def pause():
    global is_running, start_time, elapsed_time, paused_time
    if is_running:
        elapsed_time = time.time() - start_time
        is_running = False
        paused_time = elapsed_time
        log("Pause")

# Resume the timer
def resume():
    global is_running, elapsed_time, paused_time
    if not is_running:
        elapsed_time = paused_time
        is_running = True

def display_running_time(self):
    if is_running:
        return elapsed_time + (time.time() - self.start_time)
    else:
        return elapsed_time

# Write timestamps to a .txt file
def log(message):
    with open(log_file_path, "a") as log_file:
        log_file.write("{}: {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), message))

# Format time into HH:MM:SS
def format_time(seconds):
    seconds = seconds
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
        box = layout.box()

        # Display elapsed time
        box.label(text="Running Time: {:.2f} seconds" .format(display_running_time()))

        # Buttons
        layout.operator("timer.start", text="Start", icon='PLAY')
        layout.operator("timer.pause", text="Pause", icon='PAUSE')
        row = layout.row()
        row.operator("timer.resume", text="Resume", icon='RECOVER_LAST')
        row.operator("timer.stop", text="Stop", icon='SNAP_FACE')
        layout.operator("timer.display_current_time", text="Display Elapsed Time")

# Operator to start the timer
class Timer_OT_Start(bpy.types.Operator):
    bl_idname = "timer.start"
    bl_label = "Start Timer"

    def execute(self, context):
        context.scene.start()
        return {'FINISHED'}
    
# Operator to stop the timer
class Timer_OT_Stop(bpy.types.Operator):
    bl_idname = "timer.stop"
    bl_label = "Stop Timer"

    def execute(self, context):
        context.scene.stop()
        return {'FINISHED'}
    
# Operator to pause the timer
class Timer_OT_Pause(bpy.types.Operator):
    bl_idname = "timer.pause"
    bl_label = "Pause Timer"

    def execute(self, context):
        context.scene.pause()
        return {'FINISHED'}
    
# Operator to resume the timer
class Timer_OT_Resume(bpy.types.Operator):
    bl_idname = "timer.resume"
    bl_label = "Resume Timer"

    def execute(self, context):
        context.scene.resume()
        return {'FINISHED'}
    
class Timer_OT_Display(bpy.types.Operator):
    bl_idname = "timer.display"
    bl_label = "Display Current Time"

    def execute(self, context):
        context.scene.display_running_time()
        return {'FINISHED'}

# Register classes
classes = (
    PT_ProjectTimer,
    Timer_OT_Start,
    Timer_OT_Stop,
    Timer_OT_Pause,
    Timer_OT_Resume,
    Timer_OT_Display,
)

def register():
    for cls in reversed(classes):
        bpy.utils.register_class(cls)
    # Register the handler to start the timer when Blender starts or when a .blend file is loaded
    # bpy.app.handlers.load_post.append(start_timer)
    # Register the handler to close the log file when Blender exits
    # bpy.app.handlers.save_pre.append(stop_timer)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    # Unregister the handler
    # bpy.app.handlers.load_post.remove(start_timer)
    # bpy.app.handlers.save_pre.remove(stop_timer)

# def start_timer(dummy):
#     bpy.context.scene.timer.start()

# def stop_timer(dummy):
#     bpy.context.scene.timer.stop()


if __name__ == "__main__":
    register()