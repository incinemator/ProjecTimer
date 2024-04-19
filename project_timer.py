
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

class TimerPropertyGroup(bpy.types.PropertyGroup):
    """Creates a timer using python's time()"""
    start_time: bpy.props.FloatProperty(default=0)
    is_running: bpy.props.BoolProperty(default=False)
    elapsed_time: bpy.props.FloatProperty(default=0)
    paused_time: bpy.props.FloatProperty(default=0)
    log_file_path: bpy.props.StringProperty(default="timer_log.txt")


    # Start the timer
    def start(self):
        if not self.is_running:
            self.start_time = time.time()
            self.log("Start")

    # Stop the timer
    def stop(self):
        if self.start_time is not 0:
            if self.is_paused is not True and self.paused_time is not 0:
                self.elapsed_time = time.time() - self.start_time - self.paused_time
                self.start_time = 0
                self.paused_time = 0
        elif self.is_paused is not True and self.paused_time is 0:
            self.elapsed_time = time.time() - self.start_time
            self.start_time = 0
            self.paused_time = 0
        elif self.is_paused and self.paused_time is 0:
            self.elapsed_time = self.paused_time
            self.start_time = 0
            self.paused_time = 0
        elif self.is_paused and self.paused_time is not 0:
            self.elapsed_time = time.time() - self.paused_time
            self.paused_time = 0


    # Pause the timer
    def pause(self):
        if not self.is_paused:
            self.elapsed_time = time.time() - self.start_time
            self.is_paused = True
            self.paused_time = self.elapsed_time
            self.log("Pause")

    # Resume the timer
    def resume(self):
        if self.is_paused:
            self.elapsed_time = self.paused_time
            self.is_paused = False

    def display_running_time(self):
        if not self.is_paused:
            return self.elapsed_time + (time.time() - self.start_time)
        else:
            return self.elapsed_time
    
    # Write timestamps to a .txt file
    def log(self, message):
        with open(self.log_file_path, "a") as log_file:
            log_file.write("{}: {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), message))

    # Format time into HH:MM:SS
    # def format_time(self, seconds):
    #     self.seconds = seconds
    #     self.seconds = int(self.seconds % 60)
    #     self.minutes = int((self.seconds % 3600)//60)
    #     self.hours = int(self.seconds//3600)
    #     return "{:02d}:{:02d}:{:02d}".format(self.hours, self.minutes, self.seconds)
    
class TimerProperties(bpy.types.PropertyGroup):
    timer: bpy.props.PointerProperty(type=TimerPropertyGroup)
  
# UI
class PT_ProjectTimer(bpy.types.Panel):
    bl_label = "ProjecTimer"
    bl_idname = "panel.project_timer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Timer'

    def draw(self, context):
        layout = self.layout
        timer = context.scene.timer

        # Display elapsed time
        # layout.label(text="Running Time: {:.2f} seconds" .format(timer.format_time(timer.display_running_time())))
        layout.label(text="Running Time: {:.2f} seconds" .format(timer.display_running_time()))

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
        context.scene.timer.start()
        return {'FINISHED'}
    
# Operator to stop the timer
class Timer_OT_Stop(bpy.types.Operator):
    bl_idname = "timer.stop"
    bl_label = "Stop Timer"

    def execute(self, context):
        context.scene.timer.stop()
        return {'FINISHED'}
    
# Operator to pause the timer
class Timer_OT_Pause(bpy.types.Operator):
    bl_idname = "timer.pause"
    bl_label = "Pause Timer"

    def execute(self, context):
        context.scene.timer.pause()
        return {'FINISHED'}
    
# Operator to resume the timer
class Timer_OT_Resume(bpy.types.Operator):
    bl_idname = "timer.resume"
    bl_label = "Resume Timer"

    def execute(self, context):
        context.scene.timer.resume()
        return {'FINISHED'}
    
class Timer_OT_Display(bpy.types.Operator):
    bl_idname = "timer.display"
    bl_label = "Display Current Time"

    def execute(self, context):
        context.scene.timer.display_running_time()
        return {'FINISHED'}

# Register classes
classes = (
    PT_ProjectTimer,
    Timer_OT_Start,
    Timer_OT_Stop,
    Timer_OT_Pause,
    Timer_OT_Resume,
    Timer_OT_Display,
    TimerPropertyGroup
)

def register():
    for cls in reversed(classes):
        bpy.utils.register_class(cls)
    bpy.types.Scene.timer = bpy.props.PointerProperty(type=TimerPropertyGroup)
    # Register the handler to start the timer when Blender starts or when a .blend file is loaded
    bpy.app.handlers.load_post.append(start_timer)
    # Register the handler to close the log file when Blender exits
    bpy.app.handlers.save_pre.append(stop_timer)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.timer
    # Unregister the handler
    bpy.app.handlers.load_post.remove(start_timer)
    bpy.app.handlers.save_pre.remove(stop_timer)

def start_timer(dummy):
    bpy.context.scene.timer.start()

def stop_timer(dummy):
    bpy.context.scene.timer.stop()


if __name__ == "__main__":
    register()