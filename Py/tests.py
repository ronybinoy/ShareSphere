from datetime import datetime
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Hosttest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()
        
    def test_01_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)
        login=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/login/'] button.btn.btn-outline-success")
        login.click()
        time.sleep(2)
        email=driver.find_element(By.CSS_SELECTOR,"input[type='email'][name='email']")
        email.send_keys("ronybinoy189@gmail.com")
        password=driver.find_element(By.CSS_SELECTOR,"input[type='password'][name='password']")
        password.send_keys("Rony@123")
        time.sleep(2)
        submit=driver.find_element(By.CSS_SELECTOR,"button.btn-login#submitBtn")
        submit.click()
        time.sleep(2)
        chatroom=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/chatroom']")
        chatroom.click()
        time.sleep(2)
        chatstart=driver.find_element(By.CSS_SELECTOR,"a.btn.btn-primary[href='/rooms']")
        chatstart.click()
        time.sleep(2)
        room=driver.find_element(By.CSS_SELECTOR,"a.bg-primary[href='/canada/']")
        room.click()
        time.sleep(2)
        roomtext=driver.find_element(By.CSS_SELECTOR,"input[name='content']#chat-message-input")
        roomtext.send_keys("hello this is a test message")
        time.sleep(2)
        send=driver.find_element(By.CSS_SELECTOR,"button#chat-message-submit")
        send.click()
        time.sleep(2)
        roomsearch=driver.find_element(By.CSS_SELECTOR,"input#search-input")
        roomsearch.send_keys("hello")
        time.sleep(2)
        search=driver.find_element(By.CSS_SELECTOR,"button#search-button")
        search.click()
        time.sleep(2)
        more=driver.find_element(By.CSS_SELECTOR,"button#next-button.btn.btn-outline-secondary")
        more.click()
        time.sleep(2)
        more.click()
        time.sleep(2)
        roomsearch=driver.find_element(By.CSS_SELECTOR,"input#search-input")
        roomsearch.send_keys("text not in chat")
        time.sleep(2)
        search1=driver.find_element(By.CSS_SELECTOR,"button#search-button")
        search1.click()
        time.sleep(2)
        modalclose=driver.find_element(By.CSS_SELECTOR,"button.btn.bg-primary.text-white[data-dismiss='modal']")
        modalclose.click()
        time.sleep(2)
        roomclose=driver.find_element(By.CSS_SELECTOR,"button.btn.btn-danger#close-chat-room")
        roomclose.click()
        time.sleep(2)
        roomclose=driver.find_element(By.CSS_SELECTOR,"button.btn.btn-danger#close-chat-room")
        roomclose.click()
        time.sleep(2)
        profile=driver.find_element(By.CSS_SELECTOR,"a.nav-link.text-success p")
        profile.click()
        time.sleep(2)
        logout = driver.find_element(By.CSS_SELECTOR, "a.dropdown-item[href='/logout/']")
        logout.click()
        time.sleep(2)
        login=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/login/'] button.btn.btn-outline-success")
        login.click()
        time.sleep(2)
        email=driver.find_element(By.CSS_SELECTOR,"input[type='email'][name='email']")
        email.send_keys("ontario@gmail.com")
        password=driver.find_element(By.CSS_SELECTOR,"input[type='password'][name='password']")
        password.send_keys("Ontario@123")
        time.sleep(2)
        submit=driver.find_element(By.CSS_SELECTOR,"button.btn-login#submitBtn")
        submit.click()
        time.sleep(3)
        addcourse=driver.find_element(By.CSS_SELECTOR,"button.btn.btn-primary#learnMoreButton")
        addcourse.click()
        time.sleep(2)
        coursename=driver.find_element(By.CSS_SELECTOR,"input#course_name")
        coursename.send_keys("MS in computer Application")
        time.sleep(1)
        coursemode=driver.find_element(By.CSS_SELECTOR,"select#course_mode")
        coursemode.click()
        coursemodeselect=driver.find_element(By.CSS_SELECTOR,"option[value='On-campus']")
        coursemodeselect.click()
        time.sleep(1)
        coursetype=driver.find_element(By.CSS_SELECTOR,"select#course_type")
        coursetype.click()
        coursetypeselect=driver.find_element(By.CSS_SELECTOR,"option[value='Master Degree']")
        coursetypeselect.click()
        time.sleep(1)
        coursetype=driver.find_element(By.CSS_SELECTOR,"select#academic_disciplines")
        coursetype.click()
        coursetypeselect=driver.find_element(By.CSS_SELECTOR,"option[value='Engineering and Applied Science']")
        coursetypeselect.click()
        time.sleep(1)
        desc=driver.find_element(By.CSS_SELECTOR,"textarea#course_desc")
        desc.send_keys("This is a test course desc")
        time.sleep(1)
        eligibility=driver.find_element(By.CSS_SELECTOR,"textarea#eligibility")
        eligibility.send_keys("This is a test course eligibility")
        time.sleep(1)
        fees=driver.find_element(By.CSS_SELECTOR,"input#fees[type='number']")
        fees.send_keys("210")
        time.sleep(1)
        coursedur=driver.find_element(By.CSS_SELECTOR,"select#duration")
        coursedur.click()
        time.sleep(1)
        coursedurselect=driver.find_element(By.CSS_SELECTOR,"select#duration option[value='2 years']")
        coursedurselect.click()
        time.sleep(1)
        input_date1= "2023-10-20"
        formatted_date = datetime.strptime(input_date1, '%Y-%m-%d').strftime('%m-%d-%Y')
        opendate_input = driver.find_element(By.CSS_SELECTOR, "input#opendate")
        opendate_input.send_keys(formatted_date)
        time.sleep(1)
        input_date2= "2023-11-28"
        formatted_date = datetime.strptime(input_date2, '%Y-%m-%d').strftime('%m-%d-%Y')
        deaddate_input = driver.find_element(By.CSS_SELECTOR, "input#appdeadline")
        deaddate_input.send_keys(formatted_date)
        time.sleep(1)
        seats_available_input = driver.find_element(By.CSS_SELECTOR, "input#seats_available")
        seats_available_input.send_keys("20")
        time.sleep(1)
        file_path = 'C:\\Users\\Rony\\Downloads\\IT.jpeg'
        thumbnail_image_input = driver.find_element(By.CSS_SELECTOR, "input#thumbnail_image[type='file']")
        thumbnail_image_input.send_keys(file_path)
        time.sleep(3)
        submit_button = driver.find_element(By.CSS_SELECTOR, "input#submitBtn[type='submit']")
        submit_button.click()
        time.sleep(5)
        print("Added course successfully")
        manage = driver.find_element(By.CSS_SELECTOR, "a[href='/courselisting/'] button.btn.btn-primary.mt-3")
        manage.click()
        time.sleep(3)
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Optional sleep to let the page load

        # Scroll up (negative scroll distance)
        driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
        time.sleep(5)  # Optional sleep after scrolling up
        
        home = driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/institute-dashboard/']")
        home.click()

        
        
        
        
    # Add more test methods as needed

if __name__ == '__main__':
    import unittest
    unittest.main()