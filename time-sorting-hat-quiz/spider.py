import time
import scrapy
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.chrome.service as service

WAIT_TIME = 10
NUM_QUESTIONNAIRE_PAGES = 3

NUM_SAMPLE_INPUTS = 1500

class TimePotterQuizSpider(scrapy.Spider):
    name = 'timepotterquizspider'
    start_urls = ['http://time.com/4809884/harry-potter-house-sorting-hat-quiz/']
    currdir = os.path.dirname(os.path.realpath(__file__))

    def __init__(self):
        # Setting up selenium chrome env
        chromedriver_path = os.path.join(self.currdir,'../lib/chromedriver')
        os.environ["webdriver.chrome.driver"] = chromedriver_path

        # Instantiating driver
        self.driver = webdriver.Chrome(chromedriver_path)
        
    def select_questions(self, quiz_input):
        inventory_questions_element = self.driver.find_element_by_css_selector("#inventory_slide_questions > div.inventory_questions")
        inventory_questions = inventory_questions_element.find_elements_by_class_name("inventory_question")
        for inventory_question in inventory_questions:
            question_id = inventory_question.get_attribute('id')
            question_text = inventory_question.find_element_by_class_name('inventory_question_text').text
            inventory_buttons = inventory_question.find_element_by_class_name('inventory_buttons')
            value = quiz_input[question_id]
            button_to_select = inventory_buttons.find_element_by_css_selector('button:nth-child({})'.format(value))
            button_to_select.click()

    def click_next(self):
        next_button = self.driver.find_element_by_xpath('//*[@id="inventory_next"]')
        next_button.click()

    def remove_element(self, element):
        self.driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)

    def gather_results(self):
        results = {}
        house_percentages = self.driver.find_element_by_id("house_percentages")
        for house_percentage in house_percentages.find_elements_by_class_name("house_percentage"):
            percent_bar_container = house_percentage.find_element_by_class_name("percent_bar_container")
            house_percentage_label = percent_bar_container.find_element_by_class_name("house_percentage_label")
            house_name = house_percentage_label.text
            percent_bar_label = percent_bar_container.find_element_by_class_name("percent_bar_label")
            house_percent = percent_bar_label.text

            # Keep as string since we do not want to introduce needless rounding at this point
            results[house_name] = house_percent

        return results

    def kill_time_popup(self):
        try:
            popup_x = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="bx-close-inside-539747"]'))
            )

            time_offer_popup = self.driver.find_element_by_xpath('//*[@id="bx-campaign-539747"]/div[3]')
            if time_offer_popup:
                popup_x.click()
        except Exception as e:
            pass

    def kill_ads(self):
        try:
            google_ad = self.driver.find_element_by_xpath("//*[contains(@id,'google_ads_iframe_')]")
            if google_ad:
                self.remove_element(google_ad)
        except Exception as e:
            pass

        try:
            bx_shroud = self.driver.find_element_by_class_name("bx-shroud")
            if bx_shroud:
                self.remove_element(bx_shroud)
        except Exception as e:
            pass

    def click_start(self):
        start_button = WebDriverWait(self.driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="inventory_slide_sorting_hat"]/div[2]/button'))
        )
        start_button.click()

    def opt_out_demographic(self):
        non_consent_button = self.driver.find_element_by_xpath('//*[@id="hppi_consent_negative"]')
        if non_consent_button:
            non_consent_button.click()
            continue_button = self.driver.find_element_by_xpath('//*[@id="inventory_slide_intro"]/div[2]/button')
            continue_button.click()

    def select_all_questions(self, quiz_input):
        for _ in range(NUM_QUESTIONNAIRE_PAGES):
            self.select_questions(quiz_input)
            self.click_next()

    def start_quiz(self):
        # Find quiz element
        harry_potter_quiz_element = self.driver.find_element_by_xpath('//*[@id="harry_potter_house"]')

        # Navigate to quiz element
        self.driver.execute_script("arguments[0].scrollIntoView()", harry_potter_quiz_element)

        # Initiate quiz
        self.click_start()

        # Allow to initiate view
        time.sleep(1)
    
    def generate_inputs(self, n):
        import os
        import json
        from itertools import product, islice
        from random import seed, randint

        seed(42)

        with open(os.path.join(os.path.dirname(__file__), 'inputs.json')) as data_file:
            data = json.load(data_file)
            num_questions = len(data.keys())
            num_possible_answers = 7

            # Start as set to have constant time duplicate lookup
            inputs = set()
            while len(inputs) < n:
                seq = []
                for _ in range(1,num_questions+1):
                    # Create char of int sequence
                    seq.append(str(randint(1,num_possible_answers)))
                # Create string sequence so set works
                inputs.add(''.join(seq))

            # Convert unique string sequences to ints
            inputs = [map(int, list(seq)) for seq in inputs]

            # Convert into dictionary items with question keys
            inputs = [dict(zip(data.keys(), values)) for values in inputs]

            return inputs

    def parse(self, response):
        import json
        self.driver.get(self.start_urls[0])

        # Inputs will be the questions and the values given
        inputs = self.generate_inputs(NUM_SAMPLE_INPUTS)

        for qi, quiz_input in enumerate(inputs):
            # Destroy ads and popups that intefere
            self.kill_time_popup()
            self.kill_ads()

            # Start the quiz
            self.start_quiz()

            # So this data mining doesn't give spurious data to the researchers
            self.opt_out_demographic()

            # Answer the questions
            self.select_all_questions(quiz_input)

            # Gather the house percentages
            results = self.gather_results()

            data = {
                "inputs": quiz_input,
                "results": results,
            }

            with open(os.path.join(self.currdir,'data/',"{}.json".format(qi)), 'w') as df:
                json.dump(data, df)

            self.driver.refresh()

        self.driver.close()
