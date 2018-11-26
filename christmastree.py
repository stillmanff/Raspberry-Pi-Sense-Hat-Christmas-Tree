#!/usr/bin/env python

from sense_hat import SenseHat
import time
import random
from time import sleep

sense = SenseHat()

#Variables section (change these to change the way the program behaves. Let everything else alone.
#Timing parameters (how often things change)
twinkleInterval = 0.01                        #Interval in seconds between changes in any light
treetopInterval = int(1 / twinkleInterval)    #Number of seconds between top light turning on and off
treeDies = False                              #Turn a bug into a feature - if true, the tree gradually turns brown (takes about 2 days)
quietTimeStartHour = 22                       #Time to turn display off and on (mostly for people who are bugged by the lights at night)
quietTimeStartMinute = 30
activeTimeStartHour = 7
activeTimeStartMinute = 30
treeActive = True                             #Starting state of tree
treeAlwaysActive = True                       #Overrides treeActive. If on, tree is always on regardless of clock settings.
#End of variables section

#Constant section
#Colors are pretty much the best we can get
#Change all tree behaviors with these parameters
#Rules for tree pixel changing:
#1. Black pixels stay black
#2. Any pixels in row 0 stay as they are initialized
#3. All tree pixels start green.
#4. Pixels are picked at random along with a random color.
#4a. If black, they are left alone.
#4b. If green, they are changed to the random color.
#4c. If any other color, they are changed to green to preserve the basic green color of the tree.
#5. The top pixel of the tree flashes on and off red.

#Colors (note that not every integer value is available - everything rounds to nearest multiple of 4
black        = [0,0,0] # off / black
white        = [248,252,248] # white
green        = [0,252,0]     # green
brown        = [208,220,48]    # brown (Maybe look for a better brown, but there doesn't seem to be one)
red          = [252,0,0]     # red
cyan         = [0,252,252] # cyan - not used at the moment


#Feel free to change the shape of the tree. The shape will be preserved because of the rules listed above
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

#Keep going forever generating Christmas lights

topdelay = 0      #Count period for blinking top light
while True:
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
        top = sense.get_pixel(4,0)
        if top == black:
            sense.set_pixel(4,0,red)
        else:
            sense.set_pixel(4,0,black)
        topdelay = 0
    sleep(twinkleInterval)
    if (not treeAlwaysActive) & (time.localtime().tm_hour == quietTimeStartHour) & (time.localtime().tm_min == quietTimeStartMinute):    #Run this test only if we want the tree to cycle
        tree = sense.get_pixels()        #save the state of the tree
        sense.clear()                    #lights out
        treeActive = False               #Stop the show
        while not treeActive:
            sleep(30)                      #Checking twice a minute should be enough
            if (time.localtime().tm_hour == activeTimeStartHour) & (time.localtime().tm_min == activeTimeStartMinute):       #Time to start up again
                sense.set_pixels(tree)       #Restore the tree
                treeActive = True            #Restart the show
          
