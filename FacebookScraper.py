from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time


class FacebookScraper:

    # The id of an element i facebook home page that must be present (might change in the future)
    FACEBOOK_HOME_ELEMENT_ID = "facebook"
    POST_XPATH = "//div[@class='x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z' and not(contains(@class, '_4-u2'))]"
    PAGE_WAIT_TIMEOUT_SECONDS = 20

    def __init__(self, email, password, groups):
        self.email = email
        self.password = password
        self.groups = groups

    def __enter__(self):
        # Disable popups that interfere with the bot
        option = Options()
        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")
        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 1}
        )

        # Launch a Chrome browser
        self.driver = webdriver.Chrome(options=option, executable_path=ChromeDriverManager().install())
        self._login()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the browser when the script is interrupted
        self.driver.quit()

    def _login(self):
        # Navigate to the Facebook login page
        self.driver.get("https://www.facebook.com/")

        # Log in to Facebook
        email_field = self.driver.find_element_by_id("email")
        password_field = self.driver.find_element_by_id("pass")
        email_field.send_keys(self.email)
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)

        # Wait for the user's Facebook home page to load
        WebDriverWait(self.driver, FacebookScraper.PAGE_WAIT_TIMEOUT_SECONDS).until(EC.presence_of_element_located((By.ID, FacebookScraper.FACEBOOK_HOME_ELEMENT_ID)))
    
    def _get_group_posts(self, group_id):
        # Navigate to the group page
        self.driver.get(f"https://www.facebook.com/groups/{group_id}")

        # Monitor the group for posts containing the specified words
        # Wait for new posts to load
        WebDriverWait(self.driver, FacebookScraper.PAGE_WAIT_TIMEOUT_SECONDS).until(EC.presence_of_element_located((By.XPATH, FacebookScraper.POST_XPATH)))
        
        unclickable_see_more_elements = []
        see_more_elements = self.driver.find_elements_by_xpath("//*[text()='See more']")
        see_more_elements = list(set(see_more_elements) - set(unclickable_see_more_elements))
        for e in see_more_elements:
            try:
                e.click()
            except:
                unclickable_see_more_elements += [e]
                pass
        
        # Scroll the page to load all the posts
        posts = []
        WebDriverWait(self.driver, FacebookScraper.PAGE_WAIT_TIMEOUT_SECONDS).until(EC.presence_of_element_located((By.XPATH, FacebookScraper.POST_XPATH)))
        post_elements = self.driver.find_elements_by_xpath(FacebookScraper.POST_XPATH)
        # Create an ActionChains object
        actions = ActionChains(self.driver)
        for i in range(10):
            actions.move_to_element(post_elements[-1]).key_down(Keys.SHIFT).send_keys('j').key_up(Keys.SHIFT).perform()
            post_elements = self.driver.find_elements_by_xpath(FacebookScraper.POST_XPATH)
        see_more_elements = self.driver.find_elements_by_xpath("//*[text()='See more']")
        see_more_elements = list(set(see_more_elements) - set(unclickable_see_more_elements))
        for e in see_more_elements:
            try:
                e.click()
            except:
                unclickable_see_more_elements += [e]
                pass
        
        posts = [e for e in self.driver.find_elements_by_xpath(FacebookScraper.POST_XPATH) if e.text]
        import pdb; pdb.set_trace()


        # while True:
        #     WebDriverWait(self.driver, FacebookScraper.PAGE_WAIT_TIMEOUT_SECONDS).until(EC.presence_of_element_located((By.XPATH, FacebookScraper.POST_XPATH)))
        #     see_more_elements = self.driver.find_elements_by_xpath("//*[text()='See more']")
        #     see_more_elements = list(set(see_more_elements) - set(unclickable_see_more_elements))
        #     for e in see_more_elements:
        #         try:
        #             e.click()
        #         except:
        #             unclickable_see_more_elements += [e]
        #             pass

        #     post_element = self.driver.find_element_by_xpath(FacebookScraper.POST_XPATH)

        #     # Create an ActionChains object
        #     actions = ActionChains(self.driver)
        #     actions.move_to_element(post_element).key_down(Keys.SHIFT).send_keys('j').key_up(Keys.SHIFT).perform()

        #     # # Press Shift + J
        #     # actions.key_down(Keys.SHIFT).send_keys('j').key_up(Keys.SHIFT).perform()

        #     # for i in range(10):
        #     #     self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
            
        #     # see_more_elements = self.driver.find_elements_by_xpath("//*[text()='See more']")
        #     # for e in see_more_elements:
        #     #     try:
        #     #         e.click()
        #     #     except:
        #     #         self.driver.find_element_by_tag_name('body').send_keys(Keys.END)

        #     # import pdb; pdb.set_trace()
        #     # self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
        #     # time.sleep(1)
        #     # try:
        #     #     see_more_elements = self.driver.find_elements_by_xpath("//*[text()='See more']")
        #     #     for e in see_more_elements:
        #     #         try:
        #     #             e.click()
        #     #             # time.sleep(1)
        #     #         except:
        #     #             pass
        #     # except:
        #     #     pass
        #     posts = [e for e in self.driver.find_elements_by_xpath(FacebookScraper.POST_XPATH) if e.text]
        #     # # TODO: Get the "See More" text and remove the comments, like, etc.
        #     # publish_date = posts[0].get_attribute("data-utime")
        #     # import pdb; pdb.set_trace()
        #     if len(posts) >= 10:
        #         break
        
        return posts

    def get_older_posts(self):
        posts = []
        for group_id in self.groups:
                group_posts = self._get_group_posts(group_id)
                if group_posts:
                    # TODO: process posts
                    pass
                posts += group_posts
        return posts

    def run(self):
        """
        Monitor a list of groups for new posts. If a new post is found and passed the filter
        either return it or yield it and continue.
        """

        while True:
            # Navigate to groups page
            # Monitor for new posts
            pass