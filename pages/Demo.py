import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Edge()
driver.get("https://www.naukri.com/")
driver.maximize_window()



























#
# def GetUserData(csvfile,column):
#     userData = []               #Fullname,emailid,password,phoneno,workstatus,resumepath,city
#     with open(csvfile) as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             userData.append(row)
#
# csvfilepath="C:\\Users\\USER\\Demo.csv"
# for row in range(1,csvfilepath.__len__()):
#     usercredentials=GetUserData(csvfilepath,row)
#     for Fullname,emailid,password,phoneno,workstatus,resumepath,city in usercredentials:
#         driver = webdriver.Edge()
#         driver.get("https://www.naukri.com/")
#         driver.maximize_window()
#         driver.find_element(By.XPATH, '//*[@id="register_Layer"]').click()
#         fullname = driver.find_element(By.XPATH, '//*[@id="name"]').send_keys(fullname)
#         time.sleep(2)
#         # untill.is_element_present(By.XPATH,'//*[@id="register_Layer"]').click()
#         emailid = driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(emailid)
#         time.sleep(2)
#
#         password = driver.find_element(By.XPATH, '//*[@id="password"]').send_keys("Abdul@abc110107")
#         time.sleep(2)
#         mobileNumber = driver.find_element(By.XPATH, '//*[@id="mobile"]').send_keys("9494413302")
#         time.sleep(2)
#         workStatus = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div[1]/form/div[2]/div[4]/div[2]/div[2]').click()
#         time.sleep(2)
#         # uploadResume=driver.find_element(By.XPATH,'//*[@id="uploadResume"]').se
#         # time.sleep(2)
#         # location=driver.find_element(By.XPATH,'//*[@id="currentCity"]').click()
#         # driver.find_element(By.XPATH,'//*[@id="currentCity"]').send_keys("Hyderabad")
#         # time.sleep(3)
#         sendAlerts = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div[1]/form/div[2]/div[6]/a/i').click()
#         time.sleep(10)
#         RegisterNow = driver.find_element(By.XPATH)
# # Launch browser
# driver = webdriver.Edge()
# driver.get("https://www.naukri.com/")
# driver.maximize_window()
# driver.find_element(By.XPATH,'//*[@id="register_Layer"]').click()
# fullname=driver.find_element(By.XPATH,'//*[@id="name"]').send_keys("Abdul Rahim")
# time.sleep(2)
# # untill.is_element_present(By.XPATH,'//*[@id="register_Layer"]').click()
# emailid=driver.find_element(By.XPATH,'//*[@id="email"]').send_keys("abc1101@gmail.com")
# time.sleep(2)
# password=driver.find_element(By.XPATH,'//*[@id="password"]').send_keys("Abdul@abc110107")
# time.sleep(2)
# mobileNumber=driver.find_element(By.XPATH,'//*[@id="mobile"]').send_keys("9494413302")
# time.sleep(2)
# workStatus=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div[1]/form/div[2]/div[4]/div[2]/div[2]').click()
# time.sleep(2)
# uploadResume=driver.find_element(By.XPATH,'//*[@id="uploadResume"]').send_keys(resumepath)
# time.sleep(2)
# location=driver.find_element(By.XPATH,'//*[@id="currentCity"]').click()
# driver.find_element(By.XPATH,'//*[@id="currentCity"]').send_keys("Hyderabad")
# time.sleep(3)
#
# sendAlerts=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div[1]/form/div[2]/div[6]/a/i').click()
# time.sleep(10)
# RegisterNow=driver.find_element(By.XPATH)