
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
    is_paused: bpy.props.BoolProperty(default=False)
    elapsed_time: bpy.props.FloatProperty(default=0)
    paused_time: bpy.props.FloatProperty(default=0)

    # Start the timer
    def start_timer(self):
        if self.start_timer is None:
            self.start_time = time.time()
        self.is_paused = False

    # Stop the timer
    def stop_timer(self):
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

    def display_running_time(self):
        if self.start_time is not None and self.is_paused is not True:
            if self.paused_time is None:
                self.elapsed_time = time.time() - self.start_time
            elif self.paused_time is not None:
                self.resume_time = time.time()
                self.elapsed_time = time.time() - self.resume_time + self.paused_time
        return self.elapsed_time
    
    def log(self, message):
        if self.log_file is None:
            self.log_file = open("timer_log.txt", "a")
        self.log_file.write("{}: {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), message)) 

    # Format time into HH:MM:SS
    def format_time(self, seconds):
        self.seconds = seconds
        self.seconds = int(self.seconds % 60)
        self.minutes = int((self.seconds % 3600)//60)
        self.hours = int(self.seconds//3600)
        return "{:02d}:{:02d}:{:02d}".format(self.hours, self.minutes, self.seconds)
    
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

        # Display elapsed time
        layout.label(text="Running Time: {.2f} seconds" .format(context.scene.timer.format_time(context.scene.timer.display())))

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
        context.scene.start_timer()
        return {'FINISHED'}
    
# Operator to stop the timer
class Timer_OT_Stop(bpy.types.Operator):
    bl_idname = "timer.stop"
    bl_label = "Stop Timer"

    def execute(self, context):
        context.scene.stop_timer()
        return {'FINISHED'}
    
# Operator to pause the timer
class Timer_OT_Pause(bpy.types.Operator):
    bl_idname = "timer.pause"
    bl_label = "Pause Timer"

    def execute(self, context):
        context.scene.pause_timer()
        return {'FINISHED'}
    
# Operator to resume the timer
class Timer_OT_Resume(bpy.types.Operator):
    bl_idname = "timer.resume"
    bl_label = "Resume Timer"

    def execute(self, context):
        context.scene.resume_timer()
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
    TimerPropertyGroup
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.timer = bpy.props.PointerProperty(type=TimerPropertyGroup)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.timer
if __name__ == "__main__":
    register()