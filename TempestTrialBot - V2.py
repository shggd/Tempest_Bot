

import pyautogui,logging, time
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M')

class TempestBot:
    def __init__(self):
        self.game_region = None
        self.stamina_potion_used = 0


    def calculateRegion(self):
        logging.debug("Detecting Game")
        while True:#keep trying until region found
            try:
                region = pyautogui.locateOnScreen('images/top_right_corner.jpg')
                top_right = region[0] + region[2]
                top_left = region[1]
                self.game_region = (top_right - 576,top_left, 576,1024)
                time.sleep(1)
                break
            except:
                pass
        logging.debug("Game Found")

    def locateAndClick(self,images,greyscale=True,confidence=0.9):
        while True:
            try:
                position = pyautogui.locateCenterOnScreen(f'images/{images}',region=self.game_region,grayscale=greyscale,confidence=confidence)
                pyautogui.moveTo(position)
                pyautogui.click(position,duration=0.25)
                time.sleep(1)
                break
            except:
                pass

    def locate(self,images):
        try:
            position = pyautogui.locateCenterOnScreen(f'images/{images}',region=self.game_region,grayscale=True,confidence=0.9)
            return True
        except:
            return False

    def selectLunaticBattle(self):
        self.locateAndClick("lunatic_select.png",confidence=0.98)
        self.locateAndClick("fight_button.png")
        time.sleep(3)


    def checkStamina(self):
        logging.debug("Checking Stamina")
        if self.locate("restore_stamina_button.png"):
            try:
                self.locateAndClick("restore_stamina_button.png")
                self.locateAndClick("stamina_comfirmation_button.png")
                self.stamina_potion_used+=1
            except:
                logging.debug("Stamina is Fine!")

    def autoBattleSequence(self):
        while True:
            self.locateAndClick('auto_battle_button.png',greyscale=False)
            result = self.locate('auto_battle_comfirmation.png')
            if result:
                self.locateAndClick('auto_battle_comfirmation.png')
                break

    def resultCheck(self):
        time.sleep(3)
        pyautogui.click(interval=0.25)
        time.sleep(3)

        if self.locate("ok_end_button.png"): # check if trials is over
            logging.debug("Trial Over")
            self.locateAndClick("ok_end_button.png")
            return

        if self.locate("game_over_check.png"): # check if game over
            logging.debug("Game Over, Selecting new team")
            self.locateAndClick("game_over_fight_button.png",confidence=0.98)
            self.locateAndClick("game_over_fight_comfirm.png",confidence=0.98)
            self.autoBattleSequence()
        self.resultCheck()


    #default 1000 runs
    def runBot(self,round=1000):
        logging.debug(f"Running {round} trials")
        self.calculateRegion()
        while True:
            self.selectLunaticBattle()
            self.checkStamina()
            self.autoBattleSequence()
            self.resultCheck()
            round-=1
            logging.debug(f"Trial Finish, Stamina Pot used: {self.stamina_potion_used}, remaining run {round}")


if __name__ == '__main__':
    bot = TempestBot()
    bot.runBot()
