import pytest
from selenium import webdriver
from selenium.webdriver.common import actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time

# Fixture to initialize and quit the browser
@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
   # options.add_argument("--headless")  # Run in headless mode optional
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

# Positive Test Case 1: Drag and drop using drag_and_drop() method
def test_drag_and_drop_success(driver):
    driver.get("https://jqueryui.com/droppable/")
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, ".demo-frame"))
    source = driver.find_element(By.ID, "draggable")
    target = driver.find_element(By.ID, "droppable")

    actions = ActionChains(driver)
    actions.drag_and_drop(source, target).perform()
    time.sleep(1)

    assert "Dropped!" in target.text, "Drag and drop failed using drag_and_drop()."

# Positive Test Case 2: Drag and drop using click-hold-move-release sequence
def test_drag_and_drop_manual_sequence(driver):
    driver.get("https://jqueryui.com/droppable/")
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, ".demo-frame"))
    source = driver.find_element(By.ID, "draggable")
    target = driver.find_element(By.ID, "droppable")

    actions = ActionChains(driver)
    actions.click_and_hold(source).move_to_element(target).release().perform()
    time.sleep(1)

    assert "Dropped!" in target.text, "Drag and drop failed using manual click-hold-move-release."

# Negative Test Case 1: Drag partially but not into the target
def test_drag_without_drop(driver):
    driver.get("https://jqueryui.com/droppable/")
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, ".demo-frame"))
    source = driver.find_element(By.ID, "draggable")
    target = driver.find_element(By.ID, "droppable")

    actions = ActionChains(driver)
    actions.click_and_hold(source).move_by_offset(100, 0).release().perform()
    time.sleep(1)

    assert "Dropped!" not in target.text, "Drag was not on target but still registered as dropped."

#  Negative Test Case 2: Drag and drop outside any droppable target
def test_drag_and_drop_outside(driver):
    driver.get("https://jqueryui.com/droppable/")
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, ".demo-frame"))
    source = driver.find_element(By.ID, "draggable")
    target = driver.find_element(By.ID, "droppable")
    actions = ActionChains(driver)
    actions.click_and_hold(source).move_by_offset(300, 300).release().perform()
    time.sleep(1)

    assert "Dropped!" not in target.text, "Drop occurred outside target but was incorrectly accepted."
