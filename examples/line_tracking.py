'''
TPBot Edu drives along a black path.  The robot
has two infrared on its underside to keep track
of the black path.  If the left sensor does not
see the path, the right motor stops, and the robot
turns to the right until the left sensor again sees
the path. If the right sensor does not see the path,
the left motor stops, and the robot turns to the
left until the right sensor again sees the path.

NOTE:  We haven't yet told the robot what to do if
neither sensor can see the path (i.e., when the return
value from get_tracking would be 11).

'''
from tpbot_edu import *
from time import sleep

bot = TPBotEdu()

sleep(2)

while(True):
    # Get tracking information from the infrared sensors
    i = bot.get_tracking()

    # If the sensors return "01" (right sensor lost the path)
    if i == "01":
        # Stop the left motor, run the right motor at 25%.
        bot.set_motors_speed(0, 25)
    # If the sensors return "10" (the left sensor lost the path)
    if i == "10":
        # Stop the right motor, run the left motor at 25%.
        bot.set_motors_speed(25, 0)
    # If the sensors return "00" (both sensor detect the path)    
    if i == "00":
        # Keep both motors running at 25%
        bot.set_motors_speed(25, 25)  
