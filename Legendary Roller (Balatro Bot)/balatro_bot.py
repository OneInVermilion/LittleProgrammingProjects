import pyautogui as auto
import time
import pyttsx3 as voice
import operator
from pynput.keyboard import Key, Controller

time.sleep(2)
voice.speak("Start")
#print(auto.position())
#auto.screenshot("scrshot.png", region=(600, 600, 850, 270))

def reroll():
    keyb = Controller()
    keyb.press('r')
    time.sleep(1)
    keyb.release('r')
    time.sleep(3)

def checkForSoul():
    try:
        auto.locateOnScreen("Spectral_Soul.png", confidence=0.4, region=(600, 600, 850, 270))
    except auto.ImageNotFoundException:
        return False
    return True

found = False
while (not found):
    try: #click on charm tag if it exists
        auto.moveTo(tuple(map(sum, zip(auto.locateOnScreen("Charm_tag.png", confidence=0.72, region=(575, 725, 130, 130)), (150, 20)))))
        auto.click()
        time.sleep(4)
        #voice.speak("checking")
        found = checkForSoul()
        #voice.speak(found)
        if not found:
            reroll()
    except auto.ImageNotFoundException: #reroll until finds the tag
        reroll()

voice.speak("Finish")
