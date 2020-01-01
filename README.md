Just in time for Christmas, a Christmas tree with flashing colored decorations and a red star on top. The color and shape of the tree and the speed at which the colors change can be altered by changing the parameters at the top of the code. Directions are in the comments.

Revision 11/25/2018:
Discovered a bug that caused the tree to gradually turn brown. Fixed the problem but kept the behavior by creating a treeDies flag. Also responded to a request that the tree automatically go on and off on a schedule using the treeActive flag. State of the tree is saved before clearing the display, and restored when the tree restarts. Schedule for starting and stopping the tree are settable.

11/26/2018: fixed indentation bug. Removed debug code.

11/29/2018: changed sleep method to use sleep() function instead of checking time periodically.

12/4/2018: added on/off switch. Pressing the center button of the joystick turns the tree display on and off. The state is saved so it picks up where it left off. This feature is compatible with timed on/off - if the tree is turned on/off manually, it will change state at the next scheduled time. Also added comments to make the program easier to understand.

12/17/2018: LEDs are very bright, so added function to the up and down movements of the switch to exit and enter low_light mode. Note that the program is designed to be run inverted (power cable on the top of the Pi), so the down and up functions of the switch are reversed. Also changed default behavior to turn on and off once per day, instead of running all the time.

11/29/2019: Added barometer function to the flashing treetop. Flashes red for falling barometer, green for rising, white for steady. Barometer interval parameter for comparison interval. Function can be turned off using parameter.

Note: Default behavior - tree on all the time, doesn't die, top light cycles once per second with barometer function, other lights twinkle once per 0.01 second.

12/29/2019: Tuned barometer behavior, which was way too sensitive to trivial fluctuations. Barometer now averages the most recent five minutes of readings and the oldest five minutes of readings, and looks for a change of 0.01 in/hg or more. The five minute average is hardcoded but the tolerance is parameterized to allow the sensitivity of the barometer to be tuned. Changed look-back period to two hours, which is a useful length of time for comparing barometric pressures. Look-back (in seconds) is also now parameterized to allow for barometer tuning.

1/1/2020: Added double blink on flashing treetop if the barometer is rising or falling more rapidly than a settable parameter. 