import tkinter as tk
import ttkbootstrap as ttk
import time
from dataclasses import dataclass
from playsound3 import playsound

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
        self.auto_tick_id = None

        self.work = Phases("Work", 5, "primary")
        self.eyeRest = Phases("Eye Rest", 20, "success")
        self.timer = Timer([self.work, self.eyeRest])
    
        # Window Properties
        self.root.title("20-20-20 Timer")
        self.root.geometry("400x325")
        
        self._build_meter()
        self._build_buttons()
        self._build_auto_toggle()

    def _build_meter(self):
        self.meter = ttk.Meter(self.root, padding=10)
        self.meter.pack()
        self.meter.amounttotalvar.set(self.timer.currPhase.duration)
        self.set_meter_non_timer("Begin!")

    def _build_buttons(self):
        buttonsFrame = ttk.Frame(self.root, padding=10)
        # acts as the start, pause, and resume button
        self.button1 = ttk.Button(buttonsFrame, command=self.start_timer, text="Start", bootstyle="success", width=10)
        self.button1.pack(side="left", padx=10)
        # acts as the reset button
        self.button2 = ttk.Button(buttonsFrame, command=None, text="Reset", bootstyle="secondary", width = 10)
        self.button2.pack(side="right", padx=10)
        buttonsFrame.pack()

    def set_button1_start(self):
        self.button1.configure(command=self.start_timer, text="Start")

    def set_button1_continue(self):
        self.button1.configure(command=self.start_timer, text="Continue")

    def set_button1_pause(self):
        self.button1.configure(command=self.pause_timer, text="Pause")
        print("set_button1_pause ran!")

    def set_button1_resume(self):
        self.button1.configure(command=self.resume_timer, text="Resume")
        print("set_button1_resume ran!")

    def set_button2_restart(self):
        self.button2.configure(command=self.reset_timer, bootstyle="danger")

    def set_button2_none(self):
        self.button2.configure(command=None, bootstyle="secondary")

    def _build_auto_toggle(self):
        auto_toggle_frame = ttk.Frame(self.root, padding=10)
        self.auto_mode = ttk.BooleanVar()
        self.auto_toggle = ttk.Checkbutton(auto_toggle_frame, bootstyle="square toggle", variable=self.auto_mode, command=self.on_toggle)
        self.auto_toggle.pack()
        self.auto_label = ttk.Label(auto_toggle_frame, text="Auto continue", bootstyle="secondary")
        self.auto_label.pack()
        auto_toggle_frame.pack()

    def on_toggle(self):
        if not self.auto_mode.get():
            if self.auto_tick_id is not None:
                self.root.after_cancel(self.auto_tick_id)
                self.auto_tick_id = None

    def meter_tick(self):
        if self.timer.is_phase_over():
            playsound("sounds/notification.wav", block=False)
            self.timer.step_phase()
            if self.auto_mode.get():
                self.auto_tick_id = self.root.after(5000, self.start_timer)
            self.set_meter_non_timer("Complete!")
            self.set_button1_continue()
            self.set_button2_restart()
            return

        self.set_meter()
        self.tick_id = self.root.after(1000, self.meter_tick)

    def set_meter(self):
        self.meter.configure(bootstyle=self.timer.currPhase.colour, subtext=self.timer.currPhase.name)
        self.meter.amountusedvar.set(self.timer.elapsed())
        self.meter.amountuseddisplayvar.set(format_seconds(self.timer.remaining()))

    def set_meter_non_timer(self, string):
        self.meter.configure(bootstyle="secondary", amountused=1, amounttotal=1, subtext=self.timer.currPhase.name)
        self.meter.amountuseddisplayvar.set(string)
    
    def start_timer(self):
        if self.tick_id is not None:
            self.root.after_cancel(self.tick_id)
        if self.timer.isRunning:
            return
        
        self.meter.amounttotalvar.set(self.timer.currPhase.duration)
        self.set_button1_pause()
        self.set_button2_none()
        self.timer.start()
        self.meter_tick()

    def pause_timer(self):
        print("pause_timer function ran")
        if not self.timer.isRunning:
            return        
        self.root.after_cancel(self.tick_id)
        self.tick_id = None
        print("cancelled tick_id")
        self.timer.pause()
        print("cancelled timer")
        self.set_button1_resume()
        print("changed button1 to resume")
        self.set_button2_restart()

    def resume_timer(self):
        if self.timer.isRunning:
            return

        self.set_button1_pause()
        self.set_button2_none()
        self.timer.resume()
        self.meter_tick()
        print(self.timer.isRunning)

    def reset_timer(self):
        if self.timer.isRunning:
            return
        if self.tick_id is not None:
            self.root.after_cancel(self.tick_id)
            self.tick_id = None
        if self.auto_tick_id is not None:
            self.root.after_cancel(self.auto_tick_id)
            self.auto_tick_id = None
        self.timer.reset()
        self.set_button1_start()
        self.set_button2_none()
        self.set_meter_non_timer("Begin!")

    def run(self):
        self.root.mainloop()

class Timer():
    def __init__(self, phases):

        self.phases = phases
        self.currPhase = phases[0]

        self.phaseStartTime = 0
        self.pauseStartTime = None
        self.totalPauseDuration = 0

        self.isRunning = False

    def elapsed(self):
        return int(time.monotonic() - self.phaseStartTime) - self.totalPauseDuration

    def remaining(self):
        return self.currPhase.duration - self.elapsed()

    def start(self):
        self.phaseStartTime = time.monotonic()
        self.isRunning = True
        self.totalPauseDuration = 0

    def is_phase_over(self):
        return self.elapsed() >= self.currPhase.duration

    def step_phase(self):
        self.currPhase = self.phases[(self.phases.index(self.currPhase) + 1) % len(self.phases)]
        self.isRunning = False

    def pause(self):
        self.pauseStartTime = time.monotonic()
        self.isRunning = False

    def resume(self):
        pauseEndTime = time.monotonic()
        self.totalPauseDuration += int(pauseEndTime - self.pauseStartTime)
        self.pauseStartTime = None
        self.isRunning = True

    def reset(self):
        self.phaseStartTime = 0
        self.pauseStartTime = None
        self.totalPauseDuration = 0
        self.currPhase = self.phases[0]
        self.isRunning = False

def format_seconds(s):
    (mm,ss) = divmod(s, 60)
    return f"{mm}:{ss:02d}"

def main():
    myObject = Gui()
    myObject.run()

if __name__ == "__main__":
    main()