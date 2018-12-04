Just in time for Christmas, a Christmas tree with flashing colored decorations and a red star on top. The color and shape of the tree and the speed at which the colors change can be altered by changing the parameters at the top of the code. Directions are in the comments.

Revision 11/25/2018:
Discovered a bug that caused the tree to gradually turn brown. Fixed the problem but kept the behavior by creating a treeDies flag. Also responded to a request that the tree automatically go on and off on a schedule using the treeActive flag. State of the tree is saved before clearing the display, and restored when the tree restarts. Schedule for starting and stopping the tree are settable.

11/26/2018: fixed indentation bug. Removed debug code.

11/29/2018: changed sleep method to use sleep() function instead of checking time periodically.

12/4/2018: added on/off switch. Pressing the center button of the joystick turns the tree display on and off. The state is saved so it picks up where it left off. This feature is compatible with timed on/off - if the tree is turned on/off manually, it will change state at the next scheduled time. Also added comments to make the program easier to understand.

Note: Default behavior - tree on all the time, doesn't die, top light cycles once per second, other lights twinkle once per 0.01 second.
