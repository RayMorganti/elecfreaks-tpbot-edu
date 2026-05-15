"""
Set the headlight to white, wait 5 seconds, and turn off the headlight.
The 3 arguments in parentheses represent red, green and blue.  Each can
have a value between 0 and 255.
"""

from microbit import sleep
from tpbot_edu import TPBotEdu

bot = TPBotEdu()

bot.set_headlight(255, 255, 255)
sleep(5000)
bot.set_headlight(0,0,0)
