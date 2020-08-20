

import pyautogui,logging, time
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')

class TempestBot:
    def __init__(self):
        self.game_region = None
        self.stamina_potion_used = 0


    def calculateRegion(self):
        logging.debug("Calculating game region")

        region = None
        while True:
            try:
                region = pyautogui.locateOnScreen('images/top_right_corner.png')
                break
            except:
                pass

        logging.debug("Region calculate success")
        print(region)

        top_right = region[0] + region[2]
        top_left = region[1]
        self.game_region = (top_right - 576,top_left, 576,1024)
        print(self.game_region)


    def selectLunaticBattle(self):

        logging.debug("At tempest trials battle page")
        logging.debug('Selecting lunatic battle')

        self.locateAndClick("lunatic_select")
        self.locateAndClick("fight_button")

        time.sleep(5)



    def locateAndClick(self,image_name):

        while True:
            try:
                position = pyautogui.locateCenterOnScreen(f"images/{image_name}.png",region=self.game_region)
                pyautogui.moveTo(position)
                pyautogui.click(position,duration=0.25)
                break
            except:
                pass


    def checkStamina(self):
        try:
            position = pyautogui.locateCenterOnScreen(f"images/restore_stamina_button.png",region=self.game_region)
            pyautogui.moveTo(position)
            pyautogui.click(position,duration=0.25)
            time.sleep(2)
            position =pyautogui.locateCenterOnScreen(f"images/stamina_comfirmation_button.png",region=self.game_region)
            pyautogui.click(position,duration=0.25)
            self.stamina_potion_used+=1
            logging.debug("Used a Stamina pot")
        except:
            logging.debug("Stamina is Fine!")
            return


    def autoBattle(self):
        self.locateAndClick("auto_battle_button")
        self.locateAndClick("auto_battle_comfirmation")
        logging.debug("Auto Battle Begins")
        time.sleep(5)

    def resultCheck(self):
        time.sleep(5)
        pyautogui.click(interval=0.25)
        time.sleep(3)
        logging.debug("Checking WIN/Game Over ")
        try:
            position = pyautogui.locateCenterOnScreen(f"images/ok_end_button.png",region = self.game_region)
            pyautogui.moveTo(position)
            pyautogui.click(position,duration=0.25)
            return True
        except:
            pass

        try:
            position = pyautogui.locateCenterOnScreen(f"images/game_over_check.png",region = self.game_region)
            logging.debug("Game Over, continuing battle")
            self.locateAndClick("game_over_fight_button")
            self.locateAndClick("game_over_fight_comfirm")
            logging.debug("Continue auto battle")
            self.autoBattle()
        except:
            return False


    def runBot(self,round=50):
        logging.debug(f"Running {round} trials")
        bot.calculateRegion()
        while True:
            bot.selectLunaticBattle()
            bot.checkStamina()
            bot.autoBattle()
            while True:
                result = bot.resultCheck()
                if result:
                    break
            round-=1
            logging.debug(f"Trial Finish, Stamina Pot used: {self.stamina_potion_used}, remaining run{round}")


if __name__ == '__main__':

    bot = TempestBot()
    bot.runBot()

