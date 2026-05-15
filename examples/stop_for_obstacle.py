"""
The sonar sensor detects whether there is an obstacle within
stop_distance.  If there's no obstacle, the motors run forward,
the headlights are green, and a happy face is displayed on the
micro:bit screen.  If there is an obstacle, the motors stop,
the headlights turn yellow, and a sad face is displayed on the
micro:bit screen.

A sonar value of 0 is invalid.  In that case, the motors stop,
the headlights turn red, and a surprised face is displayed on the
micro:bit.
"""

from microbit import display, Image, sleep  
from tpbot_edu import *  

robot = TPBotEdu() 
stop_distance = 15

try:
    while True:
        # Read the ultrasonic distance in centimeters.
        # If you prefer distance in inches, place
        # UNIT_INCH inside the parentheses.
        distance = robot.get_distance()
        
        if distance > stop_distance:
            robot.set_motors_speed(50, 50)
            display.show(Image.HAPPY)
            robot.set_headlight(0, 255, 0)
        elif distance > 0 and distance <= stop_distance:
            robot.set_motors_speed(0,0)
            display.show(Image.SAD)
            robot.set_headlight(255, 204, 0)
        else:
            robot.set_motors_speed(0,0)
            display.show(Image.SURPRISED)
            robot.set_headlight(255, 0, 0)
        sleep(50)
                       
except Exception as error:
    robot.set_motors_speed(0,0)
    display.show(Image.SURPRISED)
    robot.set_headlight(255, 0, 0)
