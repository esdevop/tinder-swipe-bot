import os
from pathlib import Path
from dotenv import dotenv_values
from time import sleep
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.chrome import service
from selenium.webdriver.common.keys import Keys

class TinderBot():
    __FULLPATH_ENVIRONMENT = os.path.join(os.getcwd(), ".env")
    def __init__(self) -> None:
        self.FULLPATH_CHROMEDRIVER = os.path.join(os.getcwd(), "src", "driver", "chromedriver.exe")

        self.config=self.get_environment()

        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.service = service.Service(
            executable_path=self.FULLPATH_CHROMEDRIVER,
        )
        
        self.driver = webdriver.Chrome(service=self.service, port=100, options=self.options)
        print("TinderBot says Hi!")

    def get_environment(self):
        """Loads environment variables
        """
        
        envfullpath = Path(TinderBot.__FULLPATH_ENVIRONMENT)
        if not envfullpath.is_file():
            self.create_dummy_env(envfullpath)

        config = dotenv_values(".env")

        if not(config["FB_EMAIL"]):
            raise ValueError("FB_EMAIL is empty in .env. Please provide your email to login in the facebook. Example: FB_EMAIL=myemail@gmail.com")
        if not(config["FB_PASS"]):
            raise ValueError("FB_PASS is empty in .env. Please provide your email to login in the facebook. Example: FB_PASS=mypass")
        return config

    def create_dummy_env(self, envfullpath):
        """Creates a template for environment
        """
        dummy_env = "FB_EMAIL=\nFB_PASS="
        envfullpath.touch(exist_ok=True)
        with envfullpath.open("w") as env:
            env.write(dummy_env)

    def open_tinder(self):
        self.driver.get("https://tinder.com/")

        sleep(5)
        self.tinder_reject_cookies()
        self.tinder_get_to_login_options()
        sleep(2)
        self.tinder_login_with_facebook()
        sleep(10)
        self.tinder_allow_location()
        sleep(1)
        self.tinder_notallow_messages()
        sleep(5)
        ii = 0
        while ii<=2:
            sleep(3)
            self.swipe_right()
            ii+=1


    def tinder_reject_cookies(self):
        """Choose option to reject all cookies from tinder website
        """
        reject_cookies = self.driver.find_element('xpath', "/html/body/div[1]/div/div[2]/div/div/div[1]/div[2]/button")
        reject_cookies.click()

    def tinder_get_to_login_options(self):
        """Clicks login button to get to the login options
        """
        login = self.driver.find_element('xpath', "/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]")
        login.click()

    def tinder_login_with_facebook(self):
        """Use option to login with Facebook
        """
        login_with_facebook = self.driver.find_element('xpath', '/html/body/div[2]/main/div/div[1]/div/div/div[3]/span/div[2]/button/div[2]/div[2]')
        login_with_facebook.click()

        # tracking the windows: tinder and FB login popup
        tinder_window = self.driver.window_handles[0]
        fb_popup_window = self.driver.window_handles[1]

        # focus on the FB popup window
        self.driver.switch_to.window(fb_popup_window)
        fb_reject_cookies = self.driver.find_element('xpath', '/html/body/div[2]/div[2]/div/div/div/div/div[3]/button[1]')
        fb_reject_cookies.click()
        fb_email = self.driver.find_element('xpath', '/html/body/div/div[2]/div[1]/form/div/div[1]/div/input')
        fb_pass = self.driver.find_element('xpath', '/html/body/div/div[2]/div[1]/form/div/div[2]/div/input')
        fb_enter = self.driver.find_element('xpath', '/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]/input')

        fb_email.send_keys(str(self.config["FB_EMAIL"]))
        fb_pass.send_keys(str(self.config["FB_PASS"]))
        fb_enter.click()

        # focus on the tinder window
        self.driver.switch_to.window(tinder_window)

    def tinder_allow_location(self):
        """Allows Tinder to get your location
        """
        allow_location = self.driver.find_element('xpath', '/html/body/div[2]/main/div/div/div/div[3]/button[1]')
        allow_location.click()
    
    def tinder_notallow_messages(self):
        """Not allow tinder to show messages
        """
        notallow_messages = self.driver.find_element('xpath', '/html/body/div[2]/main/div/div/div/div[3]/button[2]')
        notallow_messages.click()

    def swipe_right(self):
        """Swipes right
        """
        swipe_right = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        swipe_right.send_keys(Keys.ARROW_RIGHT)


if __name__=="__main__":
    bot = TinderBot()
    bot.open_tinder()