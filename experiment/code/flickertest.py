from psychopy import visual, event, core,gui ,data,  logging, sound 
from numpy import sin, pi

time = list()

# window
window = visual.Window(
    size=(1920, 1080), fullscr=True, screen=0, 
    winype='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color='black', units='pix',
    blendMode='avg', useFBO=True)

dotFix = visual.Circle(
    win = window, units = "cm",
    radius = 0.9, fillColor = [1, 1, 1],
    lineColor=[1, 1, -1], edges = 128)

solid= visual.Circle(
    win = window, units = "cm",
    radius = 0.9, fillColor = [1, 1, 1],
    lineColor=[1, 1, -1], edges = 128)

beep = sound.Sound(
    value = 'A', secs = 0.2,
    volume = 0.5)

def audGen(): # Generate both Beep noises - one for planning and the other for movement
    beep.play()
    core.wait(1)
    beep.stop()

flicker_frequency = 1.5
current_frame = 0
trialClock=core.Clock()
timer = core.CountdownTimer(15)

while timer.getTime()>0:

    t=trialClock.getTime()
    # When to draw stimuli
    if current_frame % (2*flicker_frequency) < flicker_frequency:
        dotFix.draw()
    window.flip()
    current_frame += 1  # increment by 1
    if (t+3)%5 < 0.19:
        print("Flicker Start")
        print(t)
        solid.draw()
        window.flip()
        core.wait(3)
        
audGen()
core.wait(1)
core.quit()

