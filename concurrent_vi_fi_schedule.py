# This Python file uses the following encoding: utf-8
from __future__ import division
from psychopy import core, visual, gui, data, event
from psychopy.visual import TextStim, Rect
from psychopy.core import Clock, CountdownTimer
from psychopy.event import Mouse, getKeys
from csv import writer
from numpy.random import exponential, choice
import numpy
import os  # handy system and path functions

#cumulutive record of button presses
#data - csv with presses counts as function of time
#data are ready to visualization
#one can take derivatives from counts
#for example, rate = count/time7

#defines function to terminate script
def shutdown(filename):
    #writes array to csv
    outputWriter1 = writer(open(filename + '.csv','w'), lineterminator ='\n') 
    for i in range(0, len(data)):
        outputWriter1.writerow(data[i])
    #writes additional info to txt
    numpy.savetxt(filename + '.txt', [u"Participant: %s, Age: %s, Gender: %s. Stopped at %s." % (expInfo['participant'], expInfo['age'], expInfo['gender'], phase)], fmt='%s')
    core.quit()

#ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

#store info about the experiment session
expName = 'Concurrent variable-fixed schedule'  # from the Builder filename that created this script
expInfo = {u'participant': u'', u'gender': u'', u'age': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

#data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data' + os.path.sep + u'%s_%s' %(expInfo['participant'], expInfo['date'])

#creates window
win = visual.Window(size=(1366, 768), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color='black', colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='norm')

#system settings (session duration, interval length and size of COD)
session = 60 #minutes
phase_time = session / 6
COD = 5
schedule_list = ['ConcVI15FI15', 'ConcFI15VI15'] #where random schedule is located
interval = 15 

#initialization
#counts time from the start of reinforcement
global_time = Clock()
#timers for the schedule of reinforcement
T1, T2 = CountdownTimer(0), CountdownTimer(0)
phase_timer = CountdownTimer(0)
#tracks responses
lpressed, rpressed = False, False
mouse = Mouse()
R1, n1 = 0, 0 #tracks responses from left and prevents changeovers
R2, n2 = 0, 0 #tracks responses from right
#tracks consequences
Rf1, Rf2, score = 0, 0, 0
#tracks experiment
phase = 0 #how many different conditions introduced

data = [] #array for data
data.append(['time', 'R1', 'R2', 'Rf1', 'Rf2', 'phase', 'schedule']) #column names in csv file

#displayed text
text = TextStim(
    win = win,
    pos = (0, 0),
    text = ' '
)

#defines click boxes
lbox = Rect(
    win=win,
    width=0.3,
    height=0.3,
    lineColor='red',
    lineWidth=5,
    pos=(-0.5, -0.6)
)
rbox = Rect(
    win=win,
    width=0.3,
    height=0.3,
    lineColor='red',
    lineWidth=5,
    pos=(+0.5, -0.6)
)

#controls over experiment flow
#'q' - proceed to next phase prematurely
#'escape' - close window (with data saving and record about stopping)

#concurrent fixed-variable schedule
while global_time.getTime() < session*60:
    #draws click boxes
    lbox.draw()
    rbox.draw()
    
    #check of keyboard input
    resp_key = getKeys(['q','escape'])
    
    #proceed to next phase if 'q' is pressed or timer expires
    if 'q' in resp_key or phase_timer.getTime() < 0:
        #picks new schedule randomly
        schedule = choice(schedule_list)
        #store data
        phase += 1
        #reset system values
        T1 = CountdownTimer(0)
        T2 = CountdownTimer(0)
        n1 = 0
        n2 = 0
        #reset phase timer
        phase_timer = CountdownTimer(phase_time * 60)
    
    #process left schedule
    if mouse.isPressedIn(lbox, buttons=[0]):
        lpressed = True
    if not mouse.isPressedIn(lbox, buttons=[0]) and lpressed == True:
        lpressed = False
        R1 += 1
        n1 += 1
        #schedule of reinforcement
        n2 = 0 #reset sequence from I
        if T1.getTime() < 0 and n1 >= COD:
            score += 1
            Rf1 += 1
            n1 = 0
            #variable interval
            if schedule == 'ConcVI15FI15':
                T1 = CountdownTimer(exponential(interval))
            #fixed interval
            elif schedule == 'ConcFI15VI15':
                T1 = CountdownTimer(interval)
    
    #process right schedule
    if mouse.isPressedIn(rbox, buttons=[0]):
        rpressed = True
    if not mouse.isPressedIn(rbox, buttons=[0]) and rpressed == True:
        rpressed = False
        R2 += 1
        n2 += 1
        n1 = 0 #reset sequence from E
        if T2.getTime() < 0 and n2 >= COD:
            score += 1
            Rf2 += 1
            n2 = 0
            #variable interval
            if schedule == 'ConcVI15FI15':
                T2 = CountdownTimer(interval)
            #fixed interval
            elif schedule == 'ConcFI15VI15':
                T2 = CountdownTimer(exponential(interval))
    
    #finishes script if 'escape' pressed
    if 'escape' in resp_key:
        break
    
    #record data
    tempArray = [global_time.getTime(), R1, R2, Rf1, Rf2, phase, schedule]
    data.append(tempArray)
    
    #drawer
    text.text, text.pos = score, (0, 0)
    text.draw() #displays earned points
    if global_time.getTime() < 25.0:
        text.text = u'Кликайте внутри красных прямоугольников, чтобы заработать очки'
        text.pos = (0, +0.5)
        text.draw()

    win.flip()

final = CountdownTimer(25)

while final.getTime() > 0:
    text.text = u'Ваш результат - %i. Благодарим за участие в эксперименте. Окно закроется автоматически через %i сек.' %(score, round(final.getTime(), 0))
    text.pos = (0, 0)
    text.draw()
    
    #check of keyboard input
    resp_key = getKeys(['escape'])
    
    if 'escape' in resp_key:
        break
    
    win.flip()

#writes an array to csv and closes the window
shutdown(filename)