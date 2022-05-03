from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random

# Simulation configuration variables
# names_list = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# party_size_list = []
# for i in range(len(names_list)):
#     rand_num = random.randint(1,8)
#     party_size_list += [rand_num]
#     i += 1
# interarrival_times_list = []
# for i in range(len(names_list)):
#     rand_num = random.randint(5,30)
#     interarrival_times_list += [rand_num]
#     i += 1
# dining_time_list = []
# for i in range(len(names_list)):
#     rand_num = random.randint(45,90)
#     dining_time_list += [rand_num]
#     i += 1
# servers_list = ['01','02','03','04']
# number_of_tables_of_2 = 6
# number_of_tables_of_4 = 6
# number_of_tables_of_6 = 6
# number_of_tables_of_8 = 6

# Create your tests here.
class SimTest(LiveServerTestCase):

  def testform(self):
    selenium = webdriver.Chrome("./chromedriver.exe")
    #Choose your url to visit
    selenium.get('http://127.0.0.1:8000/waitlist/')
    #find the elements you need to submit form
    wait_name = selenium.find_element_by_id('id_name')
    wait_party_size = selenium.find_element_by_id('id_party_size')

    submit = selenium.find_element_by_id('submit_button')

    #populate the form with data
    wait_name.send_keys('Lebron James')
    wait_party_size.send_keys(2)

    #submit form
    submit.send_keys(Keys.RETURN)
    assert True



