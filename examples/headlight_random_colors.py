from microbit import sleep
from tpbot_edu import TPBotEdu
import random

bot = TPBotEdu()

while True:
    R = random.randint(0,255);
    G = random.randint(0,255);
    B = random.randint(0,255);
    bot.set_headlight(R,G,B)
    sleep(500)