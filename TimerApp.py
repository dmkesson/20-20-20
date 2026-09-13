import tkinter as tk
import ttkbootstrap as ttk
import time
from dataclasses import dataclass

@dataclass
class Phases:
    name: str
    duration: int
    colour: str

class Gui():
    def __init__(self):
        self.root = ttk.Window()

        self.tick_id = None

        self.work = Phases("Work", 1200, "primary")
        self.eyeRest = Phases("Eye Rest", 20, "success")
        self.timer = Timer([self.work, self.eyeRest])
    
        # Window Properties
        self.root.title("20-20-20 Timer")
        self.root.geometry("400x600")

        # Widgets
        self.statusLabel = ttk.Label(self.root, textvariable = self.currPhase.name)
        self.statusLabel.pack()
        
        self._build_meter()

        self.startButton = ttk.Button(self.root, command = self.start_timer, textvariable="Start")
        self.startButton.pack()

    def _build_meter(self):
        self.meter = ttk.Meter(self.root, padding = 20)
        self.meter.pack()
        self.meter.amounttotalvar.set(self.currPhase.duration)
        self.elapsed = 0
        self.remaining = self.currPhase.duration
        self.set_meter()

    def meter_tick(self):
        elapsed = int(time.monotonic() - self.phaseStart)
        self.remaining = self.currPhase.duration - self.elapsed
    
        if self.remaining <= 0:
            self.switch_phase()

        self.set_meter()
        self.tick_id = self.root.after(1000, self.meter_tick)

    def set_meter(self):
        self.meter.amountusedvar.set(self.timer.elapsed())
        self.meter.amountuseddisplayvar.set(format_seconds(self.timer.remaining()))

    def switch_phase(self):
        if self.timer.currPhase is self.work:
            self.currPhase = self.eyeRest
            self.meter.amounttotalvar.set(self.currPhase.duration)
            self.elapsed = 0
            self.remaining = self.currPhase.duration
            self.set_meter()
        else:
            self.currPhase = self.work
            self.meter.amounttotalvar.set(self.currPhase.duration)
            self.elapsed = 0
            self.remaining = self.currPhase.duration
            self.set_meter()

    def set_button(self):
        if self.timer.isRunning:
            self.root.after_cancel(self.tick_id)
            self.tick_id = None
            self.timer.isRunning = False
            
    def start_timer(self):
        if self.tick_id is not None:
            self.root.after_cancel(self.tick_id)
            
        self.timer.start_Phase()
        self.meter_tick()

    def run(self):
        self.root.mainloop()

class Timer():
    def __init__(self, phases):

        self.phases = phases
        self.currPhase = phases[0]

        self.phaseStartTime = None
        self.pauseDuration = None

        self.isRunning = False

    def elapsed(self):
        return int(time.monotonic() - self.phaseStartTime)

    def remaining(self):
        return self.currPhase.duration - self.elapsed()

    def start(self):
        self.phaseStartTime = time.monotonic()
        self.isRunning = True

    def is_phase_over(self):
        return self.elapsed() >= self.currPhase.duration

    def step_phase(self):
        self.currPhase = self.phases[(self.phases.index(self.currPhase) + 1) % len(self.phases)]

    def pause():
        pass

    def unpause():
        pass

def format_seconds(s):
    (mm,ss) = divmod(s, 60)
    return f"{mm}:{ss:02d}"

if __name__ == "__main__":
    myObject = Gui()
    myObject.run()