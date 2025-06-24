from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
import subprocess
import time 

def create_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "Android Device"
    options.no_reset = True

    driver = webdriver.Remote("http://localhost:4723", options=options)
    return driver

def wait_for_incoming_call(timeout):
    start = time.time()
    while time.time() - start < timeout:
        answer_call()
        time.sleep(1)
        if driver.current_activity == "com.android.incallui.call.InCallActivity":
            return True
    return False

def answer_call():
    subprocess.run(["adb", "shell", "input", "keyevent", "KEYCODE_HEADSETHOOK"]) 

def call(driver, number):
    driver.execute_script("mobile: shell", {
        "command": "am",
        "args": ["start", "-a", "android.intent.action.CALL", "-d", f"tel:{number}"]
    })

number_to_call = "+010123456789" # Number to call automaticaly

driver = create_driver()

print("Waiting for call incoming...")
if wait_for_incoming_call(10):
    print("Call incoming ! Answering call.")
    if driver.current_activity == "com.android.incallui.call.InCallActivity":
        print("Call successfully answered !")
else:
    print(f"No call incoming, calling {number_to_call}")
    call(driver, number_to_call)
 
driver.quit()