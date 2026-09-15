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
        self.statusLabel = ttk.Label(self.root, textvariable=self.timer.currPhase.name)
        self.statusLabel.pack()
        
        self._build_meter()

        # acts as the start, pause, and resume button
        self.buttonText1 = "Start"#
        self.buttonText2 = "Reset"
        self._build_buttons()

    def _build_meter(self):
        self.meter = ttk.Meter(self.root, padding=20)
        self.meter.pack()
        self.meter.amounttotalvar.set(self.timer.currPhase.duration)
        self.set_meter_non_timer("Begin!")

    def _build_buttons(self):
        buttonsFrame = ttk.Frame(self.root, padding=10)

        # acts as the start, pause, and resume button
        self.button1 = ttk.Button(buttonsFrame, command=self.start_timer, textvar=self.buttonText1)
        self.button1.pack(side="left", padx=10)
        # acts as the restart button
        self.button2 = ttk.Button(buttonsFrame, command=None, textvar=self.buttonText2)
        self.button2.pack(side="right", padx=10)

        buttonsFrame.pack()

    def meter_tick(self):
        if self.timer.is_phase_over():
            self.set_meter_non_timer()
            self.timer.step_phase()
            #here i need a method to wait for user input to start the next phase

        self.set_meter()
        self.tick_id = self.root.after(1000, self.meter_tick)

    def set_meter(self):
        self.meter.amountusedvar.set(self.timer.elapsed())
        self.meter.amountuseddisplayvar.set(format_seconds(self.timer.remaining()))
        self.meter.configure(bootstyle=self.timer.currPhase.colour)

    def set_meter_non_timer(self, string):
        self.meter.configure(bootstyle="secondary", amountused=1, amounttotal=1)
        self.meter.amountuseddisplayvar.set(string)

    def set_button(self):
        if self.timer.isRunning:
            self.root.after_cancel(self.tick_id)
            self.tick_id = None
            self.timer.isRunning = False
            
    def start_timer(self):
        if self.tick_id is not None:
            self.root.after_cancel(self.tick_id)
            
        self.meter.amounttotalvar.set(self.timer.currPhase.duration)
        self.timer.start()
        self.meter_tick()

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

    def pause(self):
        self.pauseStartTime = time.monotonic()
        self.isRunning = False

    def unpause(self):
        pauseEndTime = time.monotonic()
        self.totalPauseDuration += int(pauseEndTime - self.pauseStartTime)
        self.pauseStartTime = None
        self.isRunnning = True


def format_seconds(s):
    (mm,ss) = divmod(s, 60)
    return f"{mm}:{ss:02d}"

if __name__ == "__main__":
    myObject = Gui()
    myObject.run()