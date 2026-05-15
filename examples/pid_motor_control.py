"""
Control each motor using PID (Proportional-Integral-Derivative)
feedback control.
"""

from tpbot_edu import TPBotEdu, TPBotEduPIDController, SpeedUnit
from time import sleep

robot = TPBotEdu()
pid = TPBotEduPIDController(robot)

# Both wheels forward
pid.pid_speed_control(20, 20, SpeedUnit.CM_PER_SEC)

sleep(5)

# Gentle right turn
pid.pid_speed_control(25, 0, SpeedUnit.CM_PER_SEC)

sleep(5)

# Spin in place
pid.pid_speed_control(15, -15, SpeedUnit.CM_PER_SEC)

sleep(5)

pid.pid_speed_control(0, 0, SpeedUnit.CM_PER_SEC)