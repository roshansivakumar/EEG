import sys
import os
import random as rand
import numpy as np
import psychopy
from psychopy import visual, core, event, monitors, sound, clock
import serial
import time

#import eye
window = visual.Window(
    size=(1920, 1080), fullscr=False, screen=0,
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='cm')


key, allMoves,orderList,planList = [], [], [], []
trials, moves, counter = 0, 0, 0
trialBool, moveBool = False, False
order, timeSel = [i for i in range(4)], [i for i in range(6)]
planTime = [0.90, 0.95, 1.0, 1.1, 1.2, 1.3,1.35]
moveChar = ''
expClock = core.Clock()

"""
# Serial Comm
ser = serial.Serial('COM3', 9600) #manually type in port
time.sleep(2)

if sys.platform.startswith('win'):#Get port number automatically
        ports = ['COM%s' % (i + 1) for i in range(256)]

result = []
for port in ports:
    try:
        ser = serial.Serial(port)
    except (OSError, serial.SerialException):
        pass

# calibrate cameras
while(key == []):
    key = event.getKeys(keyList = ['space'])
    if(len(key)>0):
        if(key[0] == 'space'):
            core.wait(1)
            eye.calib()
            break
"""
"""Start Page"""

startText = visual.TextStim(window, font = "Arial")

startText.setText(
text = "Thank you for taking the time to participate in the experiemnt\n \
Instructions:\n \
1. You need to look at the dot for the whole experiement\n \
2. The four rectangles - representing the four directions will light up randomly\n \
Based on the sequence you must plan your movements after the first Beep\n \
3. You will need to make the movement after the second Beep which will be at random intervals\n \
4. This will repeat for 4 movments and then a new sequence of movements will light up\n \
\nNote: \n2 min breaks will be given after every 6 sequences. It would be great if you can stick to this\n \
In case you get exhausted of tired an require a break, please press the space bar. I will come and help you out.\n")
startText.setColor(color = (1, 1, 1))
startText.setPos(newPos = (0,0))
startText.setHeight(0.5)
startText.draw()

startText.setText(text = "press spacebar to start the experiement")
startText.setColor(color = (-1, -1, -1))
startText.setPos(newPos = (0, -7))
startText.setHeight(0.8)
startText.draw()

window.flip()
core.wait(3.0)

while(key == []):
    key = event.getKeys(keyList = ['space'])
    if(len(key)>0):
        if(key[0] == 'space'):
            window.flip()
            core.wait(1)
            break

"""Objects Declaration"""

# Break Text
breakText = visual.TextStim(window, font = "Arial")
breakText.setText(
    text = "sadasda")

# Dot Fixation
dotFix = visual.Circle(
    win = window, units = "cm",
    radius = 0.4, fillColor = [-1, -1, -1],
    lineColor=[-1, -1, -1], edges = 128)

# Move Indication
moveUp = visual.Rect(
    win = window, units = "cm",
    width=3, height=2, pos = (0,5),
    fillColor=[1, -1, -1], lineColor=[-1, -1, -1])

moveDown = visual.Rect(
    win = window, units = "cm",
    width=3, height=2, pos = (0,-5),
    fillColor=[1, -1, -1], lineColor=[-1, -1, -1])

moveRight = visual.Rect(
    win = window, units = "cm",
    width=3, height=2, pos = (5,0),
    fillColor=[1, -1, -1], lineColor=[-1, -1, -1])

moveLeft = visual.Rect(
    win = window, units = "cm",
    width=3, height=2, pos = (-5,0),
    fillColor=[1, -1, -1], lineColor=[-1, -1, -1])

move = [moveUp, moveDown, moveRight, moveLeft]

beep1 = sound.Sound(
    value = 'A', secs = 0.2,
    volume = 1)

beep2 = sound.Sound(
    value = 'B', secs = 0.2,
    volume = 1)


"""Function Definition"""

def to_dotScreen(): # Clear the Screen to Fixation Target
    window.flip()
    dotFix.draw()
    window.flip(clearBuffer = False)

def moveInd(): # Indicate the move direction randomly using rectangles
    rand.shuffle(order)
    orderList.append(order)
    moveAgg = [[move[order[0]]], [move[order[1]]], [move[order[2]]], [move[order[3]]]]
    allMoves.append(moveAgg)
    for i in range(4):
      for frame in range(30):
        move[order[i]].draw()
        dotFix.draw()
        window.flip(clearBuffer = True)
        dotFix.draw()
        window.flip(clearBuffer = False)
    to_dotScreen()

def audGen(): # Generate both Beep noises - one for planning and the other for movement
    beep1.play()
    rand.shuffle(planTime)
    rand.shuffle(timeSel)
    core.wait(planTime[timeSel[0]])
    planList.append(timeSel[0])
    beep1.stop()
    beep2.play()
    core.wait(0.2)
    beep2.stop()

def detMove():
    while True:
        moveStat = ser.readline()
        return moveStat

def wait():
    global key
    while(key == []):
        key = event.getKeys(keyList = ['space'])
        if(len(key)>0):
            if(key[0] == 'space'):
                window.flip()
                core.wait(1)
                break

def repeat():
    audGen()
    to_dotScreen()

trialClock=core.Clock()
while trials!=50: # From 200 trials
    t=trialClock.getTime()
    to_dotScreen()
    if trials%10 == 0 and trials != 0:
        core.wait(40)
    moves = 0
    while moves != 4: # 4 movements per trial
        if moves == 0:
            print("First move")
            print(t)
            moveInd()
            audGen()
            to_dotScreen()
            moves = moves + 1
        else:
            print(t)
            core.wait(1.7)
            audGen()
            to_dotScreen()
            moves=moves+1
    print("move completed for trial")
    print(t)
    core.wait(3)
    trials = trials + 1

print(orderList)
print(planList)
# End of experiment
window.close()
core.quit()
