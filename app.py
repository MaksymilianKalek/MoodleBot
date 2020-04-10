import selenium
from selenium import webdriver
import json

data = {}

subjects = {
  "all_subjects": ["link", "link"],
}

#Driver init
driver = webdriver.Chrome("/chromedriver.exe")
driver.maximize_window()

#Login to moodle
def login():
  driver.get("https://moodle.ue.poznan.pl/login/")

  login = driver.find_element_by_css_selector("#username")
  password = driver.find_element_by_css_selector("#password")
  btn = driver.find_element_by_css_selector("#loginbtn")

  login.send_keys("login")
  password.send_keys("password")
  btn.click()

  print("\nLogged into moodle")

login()

print()
#Compare content
with open('name.json') as f:
  new = False
  name = json.load(f)

  i = 1

  for sub in subjects:

    driver.get(subjects[sub][0])
    main = len(driver.find_elements_by_class_name("activity"))

    data[sub] = [main]

    if name[sub][0] != data[sub][0]:
      difference = data[sub][0] - name[sub][0]
      print(f"There are {difference} new things in {sub} on the main page\n")
      new = True
      driver.execute_script("window.open('');")
      driver.switch_to.window(driver.window_handles[i])
      i += 1

    driver.get(subjects[sub][1])
    disc = len(driver.find_elements_by_class_name("discussion"))

    data[sub].append(disc)

    if name[sub][1] != data[sub][1]:
      difference = data[sub][1] - name[sub][1]
      print(f"There are {difference} new things in {sub} on the discussion page\n")
      new = True
      driver.execute_script("window.open('');")
      driver.switch_to.window(driver.window_handles[i])
      i += 1

if not new:
  print("There is nothing new\n")

#Write new data
with open('name.json', 'w') as f:
  json.dump(data, f)

input("You can now close")