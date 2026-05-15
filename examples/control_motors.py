"""
Direct motor control.
Run both motors at 50% for 5 milliseconds.
Stop the left motor
Pause for 5000 milliseconds.
Stop the right motor.
Pause for 5000 milliseconds.
Start both motors again for 5000 milliseconds.
Stop both motors.
"""

from microbit import sleep
from tpbot_edu import TPBotEdu, MotorSelector

bot = TPBotEdu()

bot.set_motors_speed(50, 50)
sleep(5000)
bot.set_motor_stop(MotorSelector.LEFT)
sleep(5000)
bot.set_motor_stop(MotorSelector.RIGHT)
sleep(2000)
bot.set_motors_speed(-50, -50)
sleep(5000)
bot.set_motor_stop(MotorSelector.ALL)
