from TimerApp import Phases, Timer, format_seconds
from time import sleep

phase1 = Phases("1", 1, "abc")
phase2 = Phases("2", 5, "xyz")
#phase3 = Phases("3", 2, "hij")

def test_format_seconds():
    assert format_seconds(187) == "3:07"

def test_step_phase_first_to_second():
    myTimer = Timer([phase1, phase2])
    myTimer.step_phase()
    assert myTimer.currPhase is myTimer.phases[1]

def test_step_phase_loop():
    myTimer = Timer([phase1, phase2])
    myTimer.currPhase = myTimer.phases[-1]
    assert myTimer.currPhase is phase2
    myTimer.step_phase()
    assert myTimer.currPhase is myTimer.phases[0]

# tests remaining(), but by extension elapsed() and start()
def test_remaining():
    myTimer = Timer([phase1, phase2])
    myTimer.currPhase = myTimer.phases[1]
    myTimer.start()
    sleep(1)
    assert myTimer.remaining() == 4

def test_is_phase_over():
    myTimer = Timer([phase1, phase2])
    myTimer.start()
    sleep(1)
    assert myTimer.is_phase_over()

#new phase has correct duration and timer has reset
def test_new_phase_is_correct():
    myTimer = Timer([phase1, phase2])
    myTimer.start()
    initTime = myTimer.phaseStartTime
    sleep(2)
    assert myTimer.is_phase_over()
    myTimer.step_phase()
    myTimer.start()
    assert myTimer.currPhase.duration == 5
    assert initTime != myTimer.phaseStartTime

def test_pause_resume():
    myTimer = Timer([phase1, phase2])
    myTimer.step_phase()
    myTimer.start()
    sleep(1)
    myTimer.pause()
    assert not myTimer.isRunning 
    sleep(2)
    myTimer.resume()
    sleep(1)
    assert myTimer.currPhase is myTimer.phases[1]
    assert myTimer.totalPauseDuration == 2
    assert myTimer.remaining() == 3
    

def test_multiple_pauses():
    myTimer = Timer([phase1, phase2])
    myTimer.step_phase()
    myTimer.start()
    sleep(1)
    myTimer.pause()
    sleep(1)
    myTimer.resume()
    sleep(1)
    myTimer.pause()
    sleep(1)
    myTimer.resume()
    assert myTimer.currPhase is myTimer.phases[1]
    assert myTimer.totalPauseDuration == 2
    assert myTimer.remaining() == 3