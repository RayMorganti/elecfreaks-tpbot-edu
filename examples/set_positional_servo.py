"""
Operate a 360 degree positional (i.e., non-continuous) servo,
connected to S1.  Tested on a GeekServo 360 degree positional
servo.

When the script is run:

- the servo shaft rotates to the 90 degree position, then
- rotates to 0 after 3 seconds.

"""

from microbit import sleep, display
from tpbot_edu import TPBotEdu, ServoPort, ServoType
    
try:
    robot = TPBotEdu()
except Exception as error:
    display.scroll("init")
    print(error)

robot.set_positional_servo(ServoType.SERVO_360, ServoPort.S1, 90)
sleep(3000)
robot.set_positional_servo(ServoType.SERVO_360, ServoPort.S1, 0)
