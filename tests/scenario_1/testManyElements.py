from alumnium import Alumni
from playwright.sync_api import Page


def test_login(al: Alumni, driver: Page):
    driver.goto("http://webdriveruniversity.com/Dropdown-Checkboxes-RadioButtons/index.html")
    driver.set_viewport_size({"width": 1920, "height": 1080})


    al.do("Select 'python' from the first dropdown menu")
    al.do("Check option number 4 from the checkboxes area")
    al.do("Select 'yellow' from the radio buttons area")

    area1 = al.area("Selected & Disabled")
    area1.do("click on 'Pumpkin'")
    area1.get("Dropdown list values")


