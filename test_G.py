from alumnium import Alumni
from playwright.sync_api import Page
import time
import pandas as pd


def test_login(al: Alumni, driver: Page):
    driver.goto("https://e-services.ammancity.gov.jo/index-rtl.html")
    driver.set_viewport_size({"width": 1920, "height": 1080})

    time.sleep(10)
    al.do("type MxAdmin into 'اسم المستخدم / الرقم الوظيفي' field")
    al.do("Type P@ssw0rd into password field")
    al.do("click login button")
    time.sleep(5)


    # Open Development dropdown via JS: robust selector, scroll into view, add open + trigger click/events
    DDE = al.find("the second 'Development' list item link on the navigation bar ")
    DDE.click()
    option = al.find("option 'تسلسل إجراء خدمات التنظيم والأملاك' inside the dropdown list")
    option.click()
    


    al.do("hover on 'بحث' button")
    al.do("click on 'بحث' button")

    al.do(f"type '{subServiceType}' into 'نوع الخدمة الفرعي' field")
    al.do("hover on 'بحث' inside the box")
    al.do("click on 'بحث' button inside the box") 

    al.do("hover on 'تسلسل الإجراء الجديد' button (sub-tab)")
    al.do("click on 'تسلسل الإجراء الجديد' button (sub-tab)") 




    # dev_li = driver.locator("li.mx-navbar-item.dropdown").r(
    #     has=driver.get_by_text("Development")
    # ).first

    # dev_li.scroll_into_view_if_needed()
    # dev_li.hover()
    # dev_li.locator("a").click()


    # DDE = al.find("the link Development listitem on the upper list")
    # print(f"DDE: {DDE}")
    # print("count:", DDE.count())
    # print("visible:", DDE.is_visible())
    # print("enabled:", DDE.is_enabled())
    # DDE.click()

    # # driver.get_by_role("link", name="Development").first.hover()    
    # driver.get_by_role("link", name="Development").first.click()
    # time.sleep(5)
    # DDE = al.find("'Development' list item link on the navigation bar ")

    # al.do("hover on 'Development'list item link on the navigation bar")

    # al.do("click on 'Development'list item link on the navigation bar")

    # option = al.find("option 'تسلسل إجراء خدمات التنظيم والأملاك' inside the dropdown list")
    # al.do(f"hover on option 'تسلسل إجراء خدمات التنظيم والأملاك' {option} inside the dropdown list")
    # al.do(f"click on option 'تسلسل إجراء خدمات التنظيم والأملاك' {option} inside the dropdown list")

