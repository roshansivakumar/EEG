from psychopy import visual, event, core,gui ,data,  logging , sound
from numpy import sin, pi

# window
window = visual.Window(
    size= (1920, 1080), fullscr=True, screen=0,
    winype='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color='black', units='pix',
    blendMode='avg', useFBO=True)

dotFix = visual.Circle(
    win = window, units = "cm",
    radius = 0.9, fillColor = [1, 1, 1],
    lineColor=[1, 1, -1], edges = 128)

dotFixOdd = visual.Circle(
     win = window, units = "cm",
     radius = 1.5, fillColor = [1, -1, 0.2],
     lineColor = [1,1,-1], edges =120)

beep = sound.Sound(
    value = 'A', secs = 0.2,
    volume = 0.5)

beep2 = sound.Sound(
    value = 'D', secs = 0.2,
    volume = 0.5)

def audGen(): # Generate both Beep noises - one for planning and the other for movement
    beep.play()
    core.wait(1)
    beep.stop()

def audGen1(): # Generate both Beep noises - one for planning and the other for movement
    beep2.play()
    core.wait(1)
    beep2.stop()

flicker_frequency = 1.5
current_frame = 0
trialClock=core.Clock()
timer = core.CountdownTimer(15)

while timer.getTime()>0:
    t=trialClock.getTime()
    dotFix.draw()
    window.flip()
    core.wait(5)
    audGen()
    window.flip()

audGen1()
core.wait(1)
core.quit()
