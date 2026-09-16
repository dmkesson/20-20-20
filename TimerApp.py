import tkinter as tk
import ttkbootstrap as ttk
import time
from dataclasses import dataclass
from playsound3 import playsound

try:
    import pystray
    SYSTRAY = True
except ImportError:
    SYSTRAY = False
else:
    from threading import Thread
    from PIL import Image, ImageDraw
    from queue import Queue

@dataclass
class Phases:
    name: str
    duration: int
    colour: str

class Gui():
    def __init__(self):
        self.root = ttk.Window()

        self.tick_id = None
        # used when auto mode triggers next phase
        self.user_auto_mode = False
        self.auto_tick_id = None
        self.system_auto_mode = ttk.BooleanVar()
        self.systray_mode = ttk.BooleanVar()

        self.work = Phases("Work", 5, "primary")
        self.eye_rest = Phases("Eye Rest", 4, "success")

        self.timer = Timer([self.work, self.eye_rest])
    
        self.root.title("20-20-20 Timer")
        self.root.geometry("400x325")
        
        self._build_meter()
        self._build_buttons()
        self._build_toggles()

        if SYSTRAY:
            self.tray = Tray(self.timer)
            self.systray_queue = Queue()
            self.tray.start_thread()

    def _build_meter(self):
        self.meter = ttk.Meter(self.root, padding=10)
        self.meter.pack()
        self.meter.amounttotalvar.set(self.timer.curr_phase.duration)
        self._set_meter_non_timer("Begin!")

    def _build_buttons(self):
        buttons_frame = ttk.Frame(self.root, padding=10)
        # acts as the start, pause, and resume button
        self.button1 = ttk.Button(buttons_frame, command=self.start_timer, text="Start", bootstyle="success", width=10)
        self.button1.pack(side="left", padx=10)
        # acts as the reset button
        self.button2 = ttk.Button(buttons_frame, command=None, text="Reset", bootstyle="secondary", width = 10)
        self.button2.pack(side="right", padx=10)
        buttons_frame.pack()

    def _set_button1_start(self):
        self.button1.configure(command=self.start_timer, text="Start")

    def _set_button1_continue(self):
        self.button1.configure(command=self.start_timer, text="Continue")

    def _set_button1_pause(self):
        self.button1.configure(command=self.pause_timer, text="Pause")
        print("set_button1_pause ran!")

    def _set_button1_resume(self):
        self.button1.configure(command=self.resume_timer, text="Resume")
        print("set_button1_resume ran!")

    def _set_button2_restart(self):
        self.button2.configure(command=self.reset_timer, bootstyle="danger")

    def _set_button2_none(self):
        self.button2.configure(command=None, bootstyle="secondary")

    def _build_toggles(self):
        toggle_frame = ttk.Frame(self.root, padding=10)

        auto_toggle_frame = ttk.Frame(toggle_frame)
        self.auto_toggle = ttk.Checkbutton(auto_toggle_frame, bootstyle="square toggle", variable=self.system_auto_mode, command=self.on_auto_toggle)
        self.auto_toggle.pack()
        self.auto_label = ttk.Label(auto_toggle_frame, text="Auto continue", bootstyle="secondary")
        self.auto_label.pack()
        auto_toggle_frame.pack(side="left", padx=15, anchor="center")

        if SYSTRAY:
            systray_toggle_frame = ttk.Frame(toggle_frame)
            self.systray_toggle = ttk.Checkbutton(systray_toggle_frame, bootstyle="square toggle", variable=self.systray_mode, command=self.on_systray_toggle)
            self.systray_toggle.pack()
            self.systray_label = ttk.Label(systray_toggle_frame, text="Minimize on close", bootstyle="secondary")
            self.systray_label.pack()
            systray_toggle_frame.pack(side="right", anchor="center")

        toggle_frame.pack(anchor="center")

    def on_auto_toggle(self):
        if not self.system_auto_mode.get():
            if self.auto_tick_id is not None:
                self.root.after_cancel(self.auto_tick_id)
                self.auto_tick_id = None
            self.user_auto_mode = False
        else:
            self.user_auto_mode = True

    def on_systray_toggle(self):
        #need to turn on auto mode, grey out auto mode toggle, and remember previous user preferece
        if self.systray_mode.get():
            self.system_auto_mode.set(True)
            self.auto_toggle.state(["disabled"])
        else:
            self.auto_toggle.state(["!disabled"])
            self.system_auto_mode.set(self.user_auto_mode)

    def meter_tick(self):
        if self.timer.is_phase_over():
            playsound("sounds/notification.wav", block=False)
            self.timer.step_phase()
            if self.system_auto_mode.get():
                self.auto_tick_id = self.root.after(5000, self.start_timer)
            self._set_meter_non_timer("Complete!")
            self._set_button1_continue()
            self._set_button2_restart()
            return

        self._set_meter()
        self.tick_id = self.root.after(1000, self.meter_tick)

    def _set_meter(self):
        self.meter.configure(bootstyle=self.timer.curr_phase.colour, subtext=self.timer.curr_phase.name)
        self.meter.amountusedvar.set(self.timer.elapsed())
        self.meter.amountuseddisplayvar.set(format_seconds(self.timer.remaining()))

    def _set_meter_non_timer(self, string):
        self.meter.configure(bootstyle="secondary", amountused=1, amounttotal=1, subtext=self.timer.curr_phase.name)
        self.meter.amountuseddisplayvar.set(string)
    
    def start_timer(self):
        if self.tick_id is not None:
            self.root.after_cancel(self.tick_id)
            self.tick_id = None
        if self.auto_tick_id is not None:
            self.root.after_cancel(self.auto_tick_id)
            self.auto_tick_id = None
        if self.timer.is_running:
            return
        
        self.meter.amounttotalvar.set(self.timer.curr_phase.duration)
        self._set_button1_pause()
        self._set_button2_none()
        self.timer.start()
        self.meter_tick()

    def pause_timer(self):
        print("pause_timer function ran")
        if not self.timer.is_running:
            return        
        self.root.after_cancel(self.tick_id)
        self.tick_id = None
        print("cancelled tickId")
        self.timer.pause()
        print("cancelled timer")
        self._set_button1_resume()
        print("changed button1 to resume")
        self._set_button2_restart()

    def resume_timer(self):
        if self.timer.is_running:
            return

        self._set_button1_pause()
        self._set_button2_none()
        self.timer.resume()
        self.meter_tick()
        print(self.timer.is_running)

    def reset_timer(self):
        if self.timer.is_running:
            return
        if self.tick_id is not None:
            self.root.after_cancel(self.tick_id)
            self.tick_id = None
        if self.auto_tick_id is not None:
            self.root.after_cancel(self.auto_tick_id)
            self.auto_tick_id = None
        self.timer.reset()
        self._set_button1_start()
        self._set_button2_none()
        self._set_meter_non_timer("Begin!")

    def run(self):
        self.root.mainloop()

class Tray():
    def __init__(self, timer):
        self.timer = timer
        self.icon = pystray.Icon("20-20-20 Timer", icon=self.draw_pie(16, "blue"))

    def draw_pie(self, dimension, colour):#
        image = Image.new("RGBA", (dimension, dimension), "white")
        draw = ImageDraw.Draw(image)
        draw.pieslice([2, 2, 13, 13], 90, self._end_angle(), fill=colour, outline=colour)
        return image

    def start_thread(self):
        Thread(target=lambda: self.icon.run(), daemon=True).start()

    def _end_angle(self):
        return self.timer.elapsed_fraction() * 360 + 90

class Timer():
    def __init__(self, phases):

        self.phases = phases
        self.curr_phase = phases[0]

        self.phase_start_time = 0
        self.pause_start_time = None
        self.total_pause_duration = 0

        self.is_running = False

    def elapsed(self):
        return int(time.monotonic() - self.phase_start_time) - self.total_pause_duration

    def elapsed_fraction(self):
        return round((self.elapsed() / self.curr_phase.duration), 2)

    def remaining(self):
        return self.curr_phase.duration - self.elapsed()

    def start(self):
        self.phase_start_time = time.monotonic()
        self.is_running = True
        self.total_pause_duration = 0

    def is_phase_over(self):
        return self.elapsed() >= self.curr_phase.duration

    def step_phase(self):
        self.curr_phase = self.phases[(self.phases.index(self.curr_phase) + 1) % len(self.phases)]
        self.is_running = False

    def pause(self):
        self.pause_start_time = time.monotonic()
        self.is_running = False

    def resume(self):
        pause_end_time = time.monotonic()
        self.total_pause_duration += int(pause_end_time - self.pause_start_time)
        self.pause_start_time = None
        self.is_running = True

    def reset(self):
        self.phase_start_time = 0
        self.pause_start_time = None
        self.total_pause_duration = 0
        self.curr_phase = self.phases[0]
        self.is_running = False

def format_seconds(s):
    (mm,ss) = divmod(s, 60)
    return f"{mm}:{ss:02d}"

def main():
    my_object = Gui()
    my_object.run()

if __name__ == "__main__":
    main()