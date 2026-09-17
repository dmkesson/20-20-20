from TimerApp import Phases, Timer, format_seconds, Mode
from time import sleep

phase1 = Phases("1", 1, "abc")
phase2 = Phases("2", 5, "xyz")
phase3 = Phases("3", 3, "hij")

def test_format_seconds():
    assert format_seconds(187) == "3:07"

def test_step_phase_first_to_second():
    myTimer = Timer([phase1, phase2])
    myTimer.step_phase()
    assert myTimer.curr_phase is myTimer.phases[1]

def test_step_phase_loop():
    myTimer = Timer([phase1, phase2])
    myTimer.curr_phase = myTimer.phases[-1]
    assert myTimer.curr_phase is phase2
    myTimer.step_phase()
    assert myTimer.curr_phase is myTimer.phases[0]

def test_mode_running():
    myTimer = Timer([phase1, phase2])
    myTimer.start()
    assert myTimer.mode is Mode.RUNNING

# tests remaining(), but by extension elapsed() and start()
def test_remaining():
    myTimer = Timer([phase1, phase2])
    myTimer.curr_phase = myTimer.phases[1]
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
    initTime = myTimer.phase_start_time
    sleep(2)
    assert myTimer.is_phase_over()
    myTimer.step_phase()
    myTimer.start()
    assert myTimer.curr_phase.duration == 5
    assert initTime != myTimer.phase_start_time

def test_pause_resume():
    myTimer = Timer([phase1, phase2])
    myTimer.step_phase()
    myTimer.start()
    sleep(1)
    myTimer.pause()
    assert myTimer.mode is Mode.PAUSED
    sleep(2)
    myTimer.resume()
    sleep(1)
    assert myTimer.curr_phase is myTimer.phases[1]
    assert myTimer.total_pause_duration == 2
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
    assert myTimer.curr_phase is myTimer.phases[1]
    assert myTimer.total_pause_duration == 2
    assert myTimer.remaining() == 3

def test_reset():
    myTimer = Timer([phase1, phase2])
    myTimer.step_phase()
    myTimer.start()
    sleep(2)
    myTimer.reset()
    assert myTimer.curr_phase.duration == 1
    assert myTimer.mode is Mode.IDLE

def test_elapsed_fraction():
    myTimer = Timer([phase2, phase3])
    myTimer.start()
    sleep(1)
    assert myTimer.elapsed_fraction() == 0.2
    myTimer.step_phase()
    myTimer.start()
    sleep(1)
    assert myTimer.elapsed_fraction() == 0.33