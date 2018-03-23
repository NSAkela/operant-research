# This Python file uses the following encoding: utf-8
from __future__ import division
from psychopy import core, visual, gui, data, event
from csv import writer
import random
import numpy
import os  # handy system and path functions


#cumulutive record of button presses
#data - csv with presses counts as function of time
#data are ready to visualization
#one can take derivatives from counts
#for example, rate = count/time

#define function to terminate script
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
expName = 'Free-operant activity and feedback'  # from the Builder filename that created this script
expInfo = {u'participant': u'', u'gender': u'', u'age': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

#data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data' + os.path.sep + u'%s_%s' %(expInfo['participant'], expInfo['date'])

#create window
win = visual.Window(size=(1366, 768), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color='black', colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='norm')
#text stimulus
score_text = visual.TextStim(win, pos = (0, 0))
instruction_text = visual.TextStim(win, units = 'norm', pos = (0, +0.5))

#system settings
session = 60 #in minutes
phase_time = session / 10
feedback_list = ['FB', 'NoCounter', 'BrokenFB', 'RandomFB']
instruction_list = ['Free', 'Fixed500', 'Fixed1000']
randomization = True

#count time from experiment start
global_time = core.Clock()
phase_timer = core.CountdownTimer(0)
instruction_timer = []
#count presses
count = 0
value = 0
#count consequences
score = [] #local counter
rws = 0
pns = 0
#count phases
phase = 0
condition = []
instruction = []
i = 0
k = 1
#array for data
data = []
data.append(['time', 'responses', 'rewards', 'penalties', 'score', 'phase', 'feedback', 'instruction'])

#control over experiment flow
#'q' - proceed to next phase
#'escape' - close window (with data saving and record about stopping)

while global_time.getTime() < session * 60 and k <= len(instruction_list):
    resp_key = event.getKeys(keyList = ['e','q','escape']) #check of keyboard input
    
    #proceed to next phase if 'q' is pressed or timer expires
    if 'q' in resp_key or phase_timer.getTime() < 0:
        if randomization == True:
            #picks new schedule randomly
            feedback = random.choice(feedback_list)
            instruction = random.choice(instruction_list)
            #store data
            phase += 1
            #reset system values
            phase_timer = core.CountdownTimer(phase_time * 60)
            score = 0
            instruction_timer = core.CountdownTimer(25)
        if randomization == False:
            #picks new schedule in order
            i += 1
            if i > len(feedback_list):
                i = 1
                k += 1
            if k > len(instruction_list):
                break
            feedback = feedback_list[i - 1]
            instruction = instruction_list[k - 1]
            #store data
            phase += 1
            #reset system values
            phase_timer = core.CountdownTimer(phase_time * 60)
            score = 0
            instruction_timer = core.CountdownTimer(25)
    
    if 'e' in resp_key:
        count += 1
        if feedback == 'FB':
            score += 1
            rws += 1
        if feedback == 'NoCounter':
            score = 'NA'
        if feedback == 'BrokenFB':
            score = 0
        if feedback == 'RandomFB':
            value = numpy.random.random_integers(-1, +1)
            score += value
            if score < 0:
                score = 0
            if value == 1:
                rws += 1
            if value == -1:
                pns += 1
    
    if 'escape' in resp_key:
        break
    
    #record data
    tempArray = [round(global_time.getTime(), 6), count, rws, pns, score, phase, feedback, instruction]
    data.append(tempArray)
    
    #drawer
    score_text.setText(score)
    if 'NoCounter' in feedback:
        score_text.setText(' ')
    score_text.draw() #displays earned points
    if 'Free' in instruction:
        instruction_text.setText(u'Нажимайте клавишу E столько, сколько сможете')
    if 'Fixed500' in instruction:
        instruction_text.setText(u'Нажмите клавишу E 500 раз')
    if 'Fixed1000' in instruction:
        instruction_text.setText(u'Нажмите клавишу E 1000 раз')
    if instruction_timer.getTime() > 0: 
        instruction_text.draw()
    
    win.flip()

#writes an array to csv and closes the window
shutdown(filename)