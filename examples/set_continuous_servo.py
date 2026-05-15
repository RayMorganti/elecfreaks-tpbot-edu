"""
Note:
- This script is designed for use with a continuous rotation servo.
- Change `ServoPort.S1` to `ServoPort.S2`, `ServoPort.S3`, or
 `ServoPort.S4` if your servo is plugged into a different port.
- In this module, `set_continuous_servo(port, speed)`
  accepts speeds from `-100` to `100`.
- `0` maps to the servo stop position near `1500 µs`.
- One sign of speed will produce clockwise rotation and the other
  sign will produce counter-clockwise rotation.
"""

from microbit import sleep
from tpbot_edu import TPBotEdu, ServoPort

robot = TPBotEdu()

# Choose the servo port where the continuous rotation
# servo is connected.
servo_port = ServoPort.S1  

# If testing shows that the servo creeps at a speed of 0, you can tune the 
# stop angle in configure_continuous_servo(ServoPort.S1, stop_angle=90) 
# method.  Start with a stop angle of 92 and continuing to adjust downward 
# as needed.  This script was developed using a continuous servo that required 
# a stop angle of 88.
robot.configure_continuous_servo(ServoPort.S1, stop_angle=88)
sleep(1)

# Run the servo at full speed in one direction using
# the maximum positive speed value.
robot.set_continuous_servo(servo_port, 100)

# Keep the servo turning in that direction for 3 seconds.
sleep(3000)  

# Stop the servo again by sending the neutral speed value.
robot.set_continuous_servo(servo_port, 0)

# Wait 2 seconds so the stop action is easy to observe.
sleep(2000)  

# Run the servo at full speed in the opposite direction
# using the maximum negative speed value.
robot.set_continuous_servo(servo_port, -100)

# Keep the servo turning in the opposite direction for 3 seconds.
sleep(3000)  

# Stop the servo before trying slower speeds.
robot.set_continuous_servo(servo_port, 0)

# Wait 2 seconds so the change in motion is clear.
sleep(2000)  

# Run the servo at about half speed in the positive
# direction.
robot.set_continuous_servo(servo_port, 50)

# Keep the servo turning at this slower speed for
# 3 seconds.
sleep(3000)  

# Stop the servo once more.
robot.set_continuous_servo(servo_port, 0)

# Pause 2 seconds before the final movement.
sleep(2000)  

# Run the servo at about half speed in the negative
# direction.
robot.set_continuous_servo(servo_port, -50)

# Keep the servo turning at this slower reverse speed
# for 3 seconds.
sleep(3000)  

# Stop the servo at the end of the demonstration.
robot.set_continuous_servo(servo_port, 0)
