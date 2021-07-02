"""
bla
"""
import os
import time
import sys
import requests
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image
from datetime import datetime, timedelta
from django.test import LiveServerTestCase
from unittest import skipIf
from os import getenv

class SnapshotTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        base_dir = \
            os.sep.join(os.path.dirname(os.path.abspath(__file__)).split(os.sep)[:-1])
        os.environ["PATH"] += os.pathsep + os.path.join(base_dir, 'driver')
        driver_location = os.path.join(base_dir, 'driver', 'chromedriver.exe')
        print("====> {} ".format(driver_location))

        # take screenshot
        cls.driver = webdriver.Chrome(driver_location)
        cls.driver.implicitly_wait(10)
        super().setUpClass()


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    @skipIf(
        getenv("DJANGO_SETTINGS_MODULE") == "DigDiscord.settings.deploy_ci",
        reason="requires local driver",
    )
    def test_week_champion_snapshot(self):
        """
        champion de la semaine
        :return:
        """
        # access home page
        # url_endpoint = 'https://jean-charles-gibier.org'
        url_endpoint = 'http://127.0.0.1:8000'
        self.driver.get(url_endpoint + '/#/')
        # utilisateur
        response = None
        btuser = None
        signin = None
        input_email = None
        input_password = None
        btprofile = None
        div_alert = None
        user_token = None
        chiffres = None
        frequences = None
        secteurs = None
        histogrammes = None
        another = None
        element = None

        try:
            btuser = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (((By.XPATH, "//a[@id='__BVID__46__BV_toggle_']")))))
            btuser.click()
        except:
            self.assertIsNotNone(btuser)
        # branchement sur l'interface de login
        try:
            signin = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (((By.XPATH, "//a[contains(@class, 'dropdown-item') and text()='Sign in / Sign out']")))))
            signin.click()
        except:
            self.assertIsNotNone(signin)

        # siginin avec compte de service dans l'environnement
        try:
            input_email = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (((By.XPATH, "//input[@id='email']")))))
        except:
            self.assertIsNotNone(input_email)

        # get password handle
        try:
            input_password = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (((By.XPATH, "//input[@id='password1']")))))
        except:
            self.assertIsNotNone(input_password)

        # set password / email
        input_email.send_keys("Identifiant@Service.com")
        input_password.send_keys("Abcd1234!")

        # get profile button handle and click on it
        try:
            btprofile = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (((By.XPATH, "//button[@id='sendProfileButton']")))))
            time.sleep(5)
            btprofile.click()
        except:
            self.assertIsNotNone(btprofile)

# --------------------------------- pk x 2 ?
        # siginin avec compte de service dans l'environnement
        try:
            input_email = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (((By.XPATH, "//input[@id='email']")))))
        except:
            self.assertIsNotNone(input_email)

        # get password handle
        try:
            input_password = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (((By.XPATH, "//input[@id='password1']")))))
        except:
            self.assertIsNotNone(input_password)

        # set password / email
        input_email.send_keys("Identifiant@Service.com")
        input_password.send_keys("Abcd1234!")

        # get profile button handle and click on it
        try:
            btprofile = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (((By.XPATH, "//button[@id='sendProfileButton']")))))
            time.sleep(5)
            btprofile.click()
        except:
            self.assertIsNotNone(btprofile)

# ---------------------------------
        # get token
        try:
            div_alert = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (((By.XPATH, "//div[@id='alert']")))))
            user_token = div_alert.text
            print(" user_token : {}".format(user_token))
        except:
            print("-> user_token = {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
            self.assertIsNotNone(div_alert)

        # set the dates
        today = datetime.now()
        lastweek = today - timedelta(567)

        date_debut = datetime.strftime(lastweek, '%Y-%m-%d')
        date_fin = datetime.strftime(today, '%Y-%m-%d')
        data = json.dumps({"date_debut": date_debut, "date_fin": date_fin })
        headers = {"Authorization": 'Token '+user_token,
                   "content-type": 'application/json'}
        try:
            print(" url_endpoint : {}".format(url_endpoint))
            response = requests.put(url_endpoint + '/api/profile/44', data=data, headers=headers)
            print(" response : {}".format(response))
        except requests.exceptions.Timeout:
            print("->Timeout")
            # Maybe set up for a retry, or continue in a retry loop
        except Exception:
            print("-> user_token = {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
            self.assertIsNotNone(response)

        # chiffres
        try:
            chiffres = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (((By.XPATH, "//a[@id='__BVID__11__BV_toggle_']")))))
            chiffres.click()
        except:
            self.assertIsNotNone(chiffres)

        # test another
        try:
            another = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (((By.XPATH, "//a[contains(@class, 'dropdown-item') and text()='Bataille de mots']")))))
            another.click()
        except:
            self.assertIsNotNone(another)

        # redo
        try:
            chiffres = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (((By.XPATH, "//a[@id='__BVID__11__BV_toggle_']")))))
            chiffres.click()
        except:
            self.assertIsNotNone(chiffres)

        # frequence utilisateur
        try:
            frequences = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (((By.XPATH, "//a[contains(@class, 'dropdown-item') and text()='Fréquences utilisateurs']")))))
            frequences.click()
        except:
            self.assertIsNotNone(frequences)

        time.sleep(5)

        # secteurs
        try :
            secteurs = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (((By.XPATH, "//a[@id='__BVID__29__BV_toggle_']")))))
            secteurs.click()
        except:
            self.assertIsNotNone(secteurs)


        # histogrammes
        try :
            histogrammes = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (((By.XPATH, "//a[contains(@class, 'dropdown-item') and text()='Histogrammes']")))))
            histogrammes.click()
        except:
            self.assertIsNotNone(histogrammes)

        time.sleep(5)

        # save_screenshot
        self.driver.save_screenshot("pageImage.png")

        # element
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (((By.XPATH, "//canvas[ @id = 'bar-chart']")))))
        except:
            self.assertIsNotNone(element)

        location = element.location
        size = element.size
        # crop image
        x = location['x']
        y = location['y']
        width = location['x']+size['width']
        height = location['y']+size['height'];
        im = Image.open('pageImage.png')
        im = im.crop((int(x), int(y), int(width), int(height)))
        im.save('element.png')
