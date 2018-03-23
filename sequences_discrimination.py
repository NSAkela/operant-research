# This Python file uses the following encoding: utf-8
from __future__ import division
from psychopy import core, visual, gui, data, event
from psychopy.visual import TextStim, Rect, Window
from psychopy.core import Clock, CountdownTimer
from psychopy.event import Mouse, getKeys
from csv import writer
from numpy.random import binomial, choice
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
expName = 'Sequences discrimination'  # from the Builder filename that created this script
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

session, phases = 30, 120
R1, R2, score, phase, zeros, ones = 0, 0, 0, 0, 0, 0
lpressed, rpressed = False, False
mouse = Mouse()
stimuli_timer = CountdownTimer(0)
phase_timer = CountdownTimer(0)
global_time = Clock()
p_list = [0.25, 0.75]

data = [] #array for data
data.append(['time', 'R1', 'R2', 'score', 'number', 'zeros', 'ones', 'p']) #column names in csv file

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
    pos=(-0.3, -0.6)
)

rbox = Rect(
    win=win,
    width=0.3,
    height=0.3,
    lineColor='red',
    lineWidth=5,
    pos=(+0.3, -0.6)
)

while global_time.getTime() < session * 60:
    
    #checks of keyboard input
    resp_key = getKeys(['q','escape'])
    
    #proceeds to next phase if 'q' is pressed or timer expires
    if 'q' in resp_key or phase_timer.getTime() < 0:
        #picks new schedule randomly
        p = choice(p_list)
        #store data
        phase += 1
        #resets phase timer
        phase_timer = CountdownTimer((session / phases) * 60)
    
    #finishes script if 'escape' pressed
    if 'escape' in resp_key:
        break
    
    if stimuli_timer.getTime() < 0:
        number = binomial(1, p)
        if number == 0:
            zeros += 1
        if number == 1:
            ones += 1
        stimuli_timer = CountdownTimer(1.1)
        blank_timer = CountdownTimer(0.1)
        
    #process left schedule
    if mouse.isPressedIn(lbox, buttons=[0]):
        lpressed = True
    if not mouse.isPressedIn(lbox, buttons=[0]) and lpressed == True:
        lpressed = False
        R1 += 1
        if p == p_list[1]:
            score += 1
    
    #process right schedule
    if mouse.isPressedIn(rbox, buttons=[0]):
        rpressed = True
    if not mouse.isPressedIn(rbox, buttons=[0]) and rpressed == True:
        rpressed = False
        R2 += 1
        if p == p_list[0]:
            score += 1
    
    lbox.draw()
    rbox.draw()
    
    #target
    text.text = u'Вы часто видите число 1?'
    text.pos = (0, -0.2)
    text.draw()
    
    #responses
    text.text = u'Да'
    text.pos = (-0.3, -0.6)
    text.draw()
   
    text.text = u'Нет'
    text.pos = (+0.3, -0.6) 
    text.draw()
    
    #instructions
    if global_time.getTime() < 25:
        text.text = u'Отвечайте на вопрос, чтобы заработать очки'
    if global_time.getTime() > 25 and global_time.getTime() < 40:
        text.text = u'Вы узнаете результат в конце эксперимента'
    if global_time.getTime() > 40:
        text.text = ' '
    text.pos = (0, +0.5)
    text.draw()
        
    #stimuli
    if blank_timer.getTime() > 0:
        text.text = ' '
    if blank_timer.getTime() < 0:
        text.text = number
    text.pos = (0, 0)
    text.draw()
    
    #record data
    tempArray = [global_time.getTime(), R1, R2, score, number, zeros, ones, p]
    data.append(tempArray)
    
    win.flip()
    
final = CountdownTimer(25)

while final.getTime() > 0:
    text.text = u'Ваш результат (в баллах) - %i. Благодарим за участие в эксперименте. Окно закроется автоматически через %i сек.' % (score / 10, final.getTime())
    text.pos = (0, 0)
    text.draw()
    
    #check of keyboard input
    resp_key = getKeys(['escape'])
    
    if 'escape' in resp_key:
        break
    
    win.flip()

#writes an array to csv and closes the window
shutdown(filename)