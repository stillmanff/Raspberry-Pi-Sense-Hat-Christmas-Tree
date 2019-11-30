#!/usr/bin/env python

from sense_hat import SenseHat
import time
import random
from time import sleep

sense = SenseHat()

#Colors (note that not every integer value is available - everything rounds to nearest multiple of 4
black        = [0,0,0] # off / black
white        = [248,252,248] # white
green        = [0,252,0]     # green
brown        = [208,220,48]    # brown (Maybe look for a better brown, but there doesn't seem to be one)
red          = [252,0,0]     # red
cyan         = [0,252,252] # cyan - not used at the moment

###########################################################################################################################################
#Variables section (change these to change the way the program behaves. Let everything else alone.
#Timing parameters (how often things change)
twinkleInterval = 0.01                        #Interval in seconds between changes in any light
treetopInterval = int(1 / twinkleInterval)    #Number of seconds between top light turning on and off
treeDies = False                              #Turn a bug into a feature - if true, the tree gradually turns brown (takes about 2 days)
quietTimeStartHour = 23                       #Time to turn display off and on (mostly for people who are bugged by the lights at night)
quietTimeStartMinute = 0
activeTimeStartHour = 7
activeTimeStartMinute = 0
treeAlwaysActive = False                       #If True, tree is always on regardless of clock settings.
sense.low_light = True                        #Start with dim lights - it just looks better.
barometerInterval = 1800   # Update barometer value in seconds - twice per hour seems like a good interval
blinkingBarometer = True   # Enable tree topper as barometric pressure indicator
#End of variables section
###########################################################################################################################################

#Colors are pretty much the best we can get
#Change all tree behaviors with the above parameters
#Rules for tree pixel changing:
#1. Black pixels stay black
#2. Any pixels in row 0 stay as they are initialized
#3. All tree pixels start green.
#4. Pixels are picked at random along with a random color.
#4a. If black, they are left alone.
#4b. If green, they are changed to the random color.
#4c. If any other color, they are changed to green to preserve the basic green color of the tree.
#4d. The update interval of the tree is set by the twinkleInterval variable.
#5. The top pixel of the tree flashes on and off red.
#5a. The cycle time of the flashing red tree topper is once per second by default but can be changed with the treetopInterval variable.
#6. The tree can be set to cycle on and off once a day using the activeTime and quietTime variables.
#7. The tree can be turned on and off manually using the center button of the SenseHat joystick. This does not interrupt the timed on/off cycle.
#8. The tree display can be dimmed or brightened using the up and down functions of the SenseHat joystick.
#9. The flashing light at the top of the tree indicates rising (green), falling (red), or steady (white) barometric pressure. Pressure compared to 2 decimal places of in/Hg. Comparison time interval is settable.

#Sleep loop. This operation is complicated by the fact that neither the Python sleep() function nor the SenseHat wait_for_events() function are interruptible, so
#designing a routine that allows two different ways to interrupt the dormant stage (time and button press) is a little involved. This works, though.
#The tree is dark while executing this function.
def holdTree():           #routine to turn off tree on middle button press, then turn it back on when pressed again
    treeOff = True                                     #Flag to deal with long presses
    tree = sense.get_pixels()                          #Preserve the current tree state
    sense.clear()                                      #Turn off the tree
    sense.stick.get_events()                           #Clear all old inputs
    while treeOff:                                     #Lets us loop till the explicit set of conditions is satisfied
        sleep (0.25)                                   #Four times a second ought to be enough. Reduce CPU load.
        turnTreeOn = sense.stick.get_events()          #Would normally use wait_for_event to sleep till the button is pressed again, but need to wake up now and then to check time
        if (len(turnTreeOn) > 0) | (not(treeAlwaysActive)):     #If there may be a timed wakeup, check status whether or not the button was pressed
            passedTest = False                                  #Workaround for Python limitation - all conditions checked in compound if, even if the first is invalid and causes errors in the rest
            if (len(turnTreeOn) > 0):                           #First test: is this a button press?
                if ((turnTreeOn[len(turnTreeOn) - 1].direction == "middle") & (turnTreeOn[len(turnTreeOn) - 1].action == "released")):    #If we want timed on/off, check for button and time
                    passedTest = True
                else:
                    lightLevel(turnTreeOn)                      #Are we trying to dim or brighten the tree?
            else:
                if ((not(treeAlwaysActive)) & (time.localtime().tm_hour == activeTimeStartHour) & (time.localtime().tm_min == activeTimeStartMinute) & (time.localtime().tm_sec < 3)):    #We only test for time if the button test failed. Added a 3 second tolerance so the tree can be turned off in the first minute after turned on by timer
                    passedTest = True
                else:
                    pass
            if passedTest == True:
                treeOff = False
                sense.set_pixels(tree)                         #Restore the last state of the tree. 
                sense.stick.get_events()                       #Clear the event queue so the tree doesn't turn right off again
            else:
                pass                                           #The tree is still supposed to be off - keep going.
        else:
            pass

def lightLevel(turnTreeOn):
    #Note that the tree is meant to be run with the Pi inverted, so up is literally down. That explains the reversed logic in this method.
        if ((turnTreeOn[len(turnTreeOn) - 1].direction == "up") & (turnTreeOn[len(turnTreeOn) - 1].action == "released")):      #Up and down are switches for full light and low light
            sense.low_light = True                                                                                                #Dim display (up is actually down)
        elif ((turnTreeOn[len(turnTreeOn) - 1].direction == "down") & (turnTreeOn[len(turnTreeOn) - 1].action == "released")):     
            sense.low_light = False                                                                                               #Bright display (down is actually up)
        else:
            pass

def mToi(pValue):
    answer = pValue * 0.0295301
    return answer


def initBarometer(baromArr, baromInt):
    currentPressure = int(mToi(sense.get_pressure()) * 100) / 100.
    i = int(baromInt) + 1       #Initialize the array to the number of one-second slots we'll need
    baromArr = [currentPressure] * i
    return baromArr

def shiftPressures(baromArr, currPress):     #shift all historic barometer values to the left
    for i in range (1, len(baromArr)):
        baromArr[i - 1] = baromArr[i]
        baromArr[len(baromArr) - 1] = currPress
    return baromArr

barometerTimer = 0      #Initialize counter
currentPressure = int(mToi(sense.get_pressure()) * 100) / 100.

pressureArray = []                                              #Define array for barometric pressure - will be a sliding window that updates every minute
pressureArray = initBarometer(pressureArray, barometerInterval) #Start with the same value every minute. Eventually we'll be able to look back once a minute to the value a barometerInterval ago.
#print pressureArray, len(pressureArray)

#Feel free to change the shape of the tree. The shape you choose will be preserved because of the rules listed above
#  but the colors of individual pixels will flicker between green and a random color.

tree = [
    black,black,black,black,black,black,black,black,
    black,black,black,black,green,black,black,black,
    black,black,black,green,green,green,black,black,
    black,black,green,green,green,green,green,black,
    black,green,green,green,green,green,green,green,
    green,green,green,green,green,green,green,green,
    black,black,green,green,green,green,green,black,
    black,black,black,brown,brown,brown,black,black
    ]

#Draw the tree
pixeloffset = 0
index = 0
sense.set_rotation(180) # Optional
sense.set_pixels(tree)

#Main method to update the colors on the tree. The tree is light while in this section of the code.

topdelay = 0      #Count period for blinking top light
while True:
    switchOff = sense.stick.get_events()     #Has the button been pressed to turn the tree off?
    if len(switchOff) > 0:
        if (switchOff[len(switchOff) - 1].direction == "middle") & (switchOff[len(switchOff) - 1].action == "released"):    #Was the middle button pressed?
            holdTree()
        else:
            lightLevel(switchOff)              #Are we trying to dim or brighten the tree?
    randx = random.randint(0,7)        #X position
    randy = random.randint(0,6)        #Y position - don't cover the trunk (row 7)
    randr = random.randint(4,252)      #red component of new color (anything less than 4 rounds to 0)
    randg = random.randint(4,252)      #green component of new color
    randb = random.randint(4,252)      #blue component of new color
    pixel = sense.get_pixel(randx,randy)
    if (randx == 4) and (randy == 0):    #This is the treetop, we deal with it below
        pass
    elif pixel == black:             #Leave background pixels alone 
        pass
    #Use this clause only if treeDies is true. The tree eventually all turns brown. Trunk is protected now by exempting the bottom row from selection.
    elif treeDies & (pixel == brown):           #Leave the trunk alone
        pass
    elif pixel == green:            #Turn green pixels into random christmas lights
        sense.set_pixel(randx,randy,randr,randb,randg)
    else:                          #This is already a christmas light. Turn it green again.
        sense.set_pixel(randx,randy,green)
    topdelay = topdelay + 1
    #This is the number of twinkles between treetop updates, connected to the update interval. Should be about 1 second per update.
    if topdelay == treetopInterval:
        if blinkingBarometer:
####New code to get the treetop to blink different colors for barometric pressure
            currentPressure = int(mToi(sense.get_pressure()) * 100) / 100.   #make sure the change is significant - two decimal places
            pressureArray = shiftPressures(pressureArray, currentPressure)                  #put the new pressure at the end of the array
            oldPressure = pressureArray[0]                                  #look back as far as possible
            #                print oldPressure, currentPressure, pressureArray
            #                currentPressure = currentPressure * (random() + 0.5)
            #                print oldPressure, currentPressure
            if oldPressure > currentPressure:
                dotColor = red          #pressure falling
            elif oldPressure < currentPressure:
                dotColor = green        #Pressure rising
            else:
                dotColor = white        #Pressure steady (within margin of error)
        else:
            dotColor = red
####end of barometer code

        top = sense.get_pixel(4,0)
        if top == black:
            sense.set_pixel(4,0,dotColor)
        else:
            sense.set_pixel(4,0,black)
        topdelay = 0
    sleep(twinkleInterval)
    if (not treeAlwaysActive) & (time.localtime().tm_hour == quietTimeStartHour) & (time.localtime().tm_min == quietTimeStartMinute) & (time.localtime().tm_sec < 3):    #Run this test only if we want the tree to cycle. 3 second window for timer allows activation of button quickly but avoids likely collisions.
        holdTree()                       #Go into wait routine


#This code obsolete, but keeping it around in case we have to calculate sleep interval for some other purpose.

#        sleepMinutes = (activeTimeStartMinute - quietTimeStartMinute)    #how many seconds in the last hour of sleep
#        sleepHours = (activeTimeStartHour - quietTimeStartHour)     #How many integer hours to sleep, in seconds
#        if sleepHours < 0:
#            sleepHours = sleepHours + 24                          #Add a day in seconds
#        if sleepMinutes > 0:
#            sleepSeconds = (sleepHours * 3600) + (sleepMinutes * 60)                          #Add to minutes if it's positive
#        else:
#            sleepMinutes = 60 + sleepMinutes                                #Subtract the balance of the hour from the total hours
#            sleepSeconds = ((sleepHours - 1) * 3600) + (sleepMinutes * 60)
#        #print "Hours = " + str(sleepHours) + ", Minutes = " + str(sleepMinutes) + ", seconds = " + str(sleepSeconds) + " Total time " + str(sleepSeconds / 3600) + ":" + str((sleepSeconds / 60) % 60)
#        sleep(sleepSeconds)                                                   #Go to sleep
#        treeActive = True
#        sense.set_pixels(tree)
