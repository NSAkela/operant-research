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
schedule_list = ['ConcChFR20VI10/FR20FI10', 'ConcChFR20FI10/FR20VI10'] #where random schedule is located
interval = 10
ratio = 20
link_time = 100
initial = False

#initialization
#counts time from the start of reinforcement
global_time = Clock()
#timers for the schedule of reinforcement
interval_timer = CountdownTimer(0)
phase_timer = CountdownTimer(0)
link_timer = CountdownTimer(0)
#tracks responses
lpressed, rpressed, cpressed = False, False, False
mouse = Mouse()
R1, n1 = 0, 0 #tracks responses from left and prevents changeovers
R2, n2 = 0, 0 #tracks responses from right
R3, n3 = 0, 0 #tracks responses from center
#tracks consequences
Cs1, Cs2, Cs3, score = 0, 0, 0, 0
#tracks experiment
phase = 0 #how many different conditions introduced

data = [] #array for data
data.append(['time', 'R1', 'n1', 'Cs1', 'R2', 'n2', 'Cs2', 'R3', 'n3', 'Cs3', 'score', 'phase', 'schedule']) #column names in csv file

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

cbox = Rect(
    win=win,
    width=0.3,
    height=0.3,
    lineColor='red',
    lineWidth=5,
    pos=(0.0, -0.6)
)

#controls over experiment flow
#'q' - proceed to next phase prematurely
#'escape' - close window (with data saving and record about stopping)

#chained concurrent fixed-variable schedule (sampling with replacement)
while global_time.getTime() < session * 60:
    
    #checks of keyboard input
    resp_key = getKeys(['q','escape'])
    
    #proceeds to next phase if 'q' is pressed or timer expires
    if 'q' in resp_key or phase_timer.getTime() < 0:
        #picks new schedule randomly
        schedule = choice(schedule_list)
        #store data
        phase += 1
        #resets system values
        n1 = 0
        n2 = 0
        n3 = 0
        #resets phase timer
        phase_timer = CountdownTimer(phase_time * 60)
        link_timer = CountdownTimer(link_time)
        
    #finishes script if 'escape' pressed
    if 'escape' in resp_key:
        break
    
    if link_timer.getTime() < 0:
        n1 = 0
        n2 = 0
        n3 = 0
        link_timer = CountdownTimer(link_time)
        interval_timer = CountdownTimer(0)
    
    #processes initial link schedule
    if n1 < ratio and n2 < ratio:
        
        initial = True
        
        #draws click boxes
        lbox.draw()
        rbox.draw()
        
        if mouse.isPressedIn(lbox, buttons=[0]):
            lpressed = True
        if not mouse.isPressedIn(lbox, buttons=[0]) and lpressed == True:
            lpressed = False
            R1 += 1
            n1 += 1
            Cs1 += 1
            n2 = 0 #resets sequence from right
        
        if mouse.isPressedIn(rbox, buttons=[0]):
            rpressed = True
        if not mouse.isPressedIn(rbox, buttons=[0]) and rpressed == True:
            rpressed = False
            n1 = 0
            R2 += 1
            n2 += 1
            Cs2 += 1
        
        text.text = n1
        text.pos = (-0.5, +0.25)
        text.draw()
        
        text.text = n2
        text.pos = (+0.5, +0.25)
        text.draw()
    
    #processes terminal link schedule
    if n1 >= ratio or n2 >= ratio:
        
        #resets timer for the first time
        if initial == True:
            if schedule == 'ConcChFR20VI10/FR20FI10':
                interval_timer = CountdownTimer(exponential(interval))
            if schedule == 'ConcChFR20FI10/FR20VI10':
                interval_timer = CountdownTimer(interval)
            initial = False
        
        cbox.draw()
        
        #processes left schedule
        if mouse.isPressedIn(cbox, buttons=[0]):
            cpressed = True
        if not mouse.isPressedIn(cbox, buttons=[0]) and cpressed == True:
            cpressed = False
            R3 += 1
            #schedule of reinforcement
            if interval_timer.getTime() < 0:
                n3 += 1
                Cs3 += 1
                score += 1
                if n1 >= ratio:
                    if schedule == 'ConcChFR20VI10/FR20FI10':
                        interval_timer = CountdownTimer(exponential(interval))
                    if schedule == 'ConcChFR20FI10/FR20VI10':
                        interval_timer = CountdownTimer(interval)
                if n2 >= ratio:
                    if schedule == 'ConcChFR20VI10/FR20FI10':
                        interval_timer = CountdownTimer(interval)
                    if schedule == 'ConcChFR20FI10/FR20VI10':
                        interval_timer = CountdownTimer(exponential(interval))
        
        text.text = n3
        text.pos = (0, +0.25)
        text.draw()
    
    text.text = u'Очки: %i' %score
    text.pos = (-0.75, +0.75)
    text.draw()
    
    if global_time.getTime() < 25.0:
        text.text = u'Кликайте на прямоугольники, чтобы заработать очки'
        text.pos = (0, + 0.5)
        text.draw()
    
    #record data
    tempArray = [global_time.getTime(), R1, n1, Cs1, R2, n2, Cs2, R3, n3, Cs3, score, phase, schedule]
    data.append(tempArray)

    win.flip()

final = CountdownTimer(25)

while final.getTime() > 0:
    text.text = u'Ваш результат - %i. Благодарим за участие в эксперименте. Окно закроется автоматически через %i сек.' % (score, round(final.getTime(), 0))
    text.pos = (0, 0)
    text.draw()
    
    #check of keyboard input
    resp_key = getKeys(['escape'])
    
    if 'escape' in resp_key:
        break
    
    win.flip()

#writes an array to csv and closes the window
shutdown(filename)