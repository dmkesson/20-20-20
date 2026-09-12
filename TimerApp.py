import tkinter as tk
import ttkbootstrap as ttk
import time
from dataclasses import dataclass

@dataclass
class Status:
    name: str
    duration: int
    colour: str

class EyeTimer():
    def __init__(self):
        self.root = ttk.Window()

        self.work = Status("Work", 1200, "primary")
        self.eyeRest = Status("Eye Rest", 20, "success")
        self.currStatus = self.work
        self.timerRunning = False

        self.phaseStart = 0
        self.elapsed = 0
        self.remaining = 100000
        self.tick_id = None
    
        # Window Properties
        self.root.title("20-20-20 Timer")
        self.root.geometry("400x600")

        # Widgets
        self.statusLabel = ttk.Label(self.root, textvariable = self.currStatus.name)
        self.statusLabel.pack()
        
        self.init_meter()

        self.startButton = ttk.Button(self.root, command = self.start_timer, textvariable="Start")
        self.startButton.pack()

    def init_meter(self):
        self.meter = ttk.Meter(self.root, padding = 20)
        self.meter.pack()
        self.meter.amounttotalvar.set(self.currStatus.duration)
        self.elapsed = 0
        self.remaining = self.currStatus.duration
        self.set_meter()

    def meter_tick(self):
        self.elapsed = int(time.monotonic() - self.phaseStart)
        self.remaining = self.currStatus.duration - self.elapsed
    
        if self.remaining <= 0:
            self.switch_phase()

        self.set_meter()
        self.tick_id = self.root.after(1000, self.meter_tick)

    def set_meter(self):
        (mm,ss) = divmod(self.remaining, 60)
        self.meter.amountusedvar.set(self.elapsed)
        self.meter.amountuseddisplayvar.set(f"{mm}:{ss:02d}")

    def switch_phase(self):
        if self.currStatus is self.work:
            self.currStatus = self.eyeRest
            self.meter.amounttotalvar.set(self.currStatus.duration)
            self.elapsed = 0
            self.remaining = self.currStatus.duration
            self.set_meter()
        else:
            self.currStatus = self.work
            self.meter.amounttotalvar.set(self.currStatus.duration)
            self.elapsed = 0
            self.remaining = self.currStatus.duration
            self.set_meter()

    def set_button(self):
        if timerRunning:
            self.root.after_cancel(self.tick_id)
            self.tick_id = None
            timerRunning = False
            



    # set the meter total, check the current time for time elapsed, call the after function and reset the timer
    def start_timer(self):
        if self.tick_id is not None:
            self.root.after_cancel(self.tick_id)
            
        self.phaseStart = time.monotonic()
        self.meter_tick()

    def run(self):
        self.root.mainloop()


myObject = EyeTimer()

myObject.run()