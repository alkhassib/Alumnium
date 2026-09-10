from alumnium import Alumni
from playwright.sync_api import Page
import time
import pandas as pd

global df
global Data
global DataRows
global subServiceType

subServiceType = "خدمة تعديل تنظيمي"

df = pd.read_excel(r"tests/scenario_1/Dummt.xlsx")
Data = df.to_dict('records')
DataRows = len(Data)

def test_login(al: Alumni, driver: Page):
    driver.goto("http://10.35.24.158:8081/index-rtl.html")
    driver.set_viewport_size({"width": 1920, "height": 1080})

    time.sleep(12)
    # تسجيل الدخول
    al.do("type MxAdmin into 'اسم المستخدم / الرقم الوظيفي' field")
    al.do("Type 123456789Aa@ into password field")
    al.do("click login button")
    print("تم تسجيل الدخول")

    global df
    global Data
    global DataRows
    global subServiceType



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

    # for i in range(DataRows):
    for i in range(2):
        ActionTypeCode= Data[i]['ActionTypeCode']
        FromStatusCode= Data[i]['FromStatusCode']
        FromRole= Data[i]['FromRole']
        ToStatusCode= Data[i]['ToStatusCode']
        ToRole= Data[i]['ToRole']
        MainStatusCode= Data[i]['MainStatusCode']
        InboxStatus= Data[i]['InboxStatus']  
        print(f"ActionTypeCode: {ActionTypeCode}")
        print(f"FromStatusCode: {FromStatusCode}")
        print(f"FromRole: {FromRole}")
        print(f"ToStatusCode: {ToStatusCode}")
        print(f"ToRole: {ToRole}")
        print(f"MainStatusCode: {MainStatusCode}")
        print(f"InboxStatus: {InboxStatus}")
        print("_____________________________________")
        try: 
            al.do("hover on 'جديد' button")
            al.do("click on 'جديد' button")

            print(f"{i} record started")
            PopupArea = al.area("'إضافة - تعديل تسلسل الإجراء' popup")

            PopupArea.do("hover on the button of 'نوع الإجراء' field ")
            PopupArea.do("click on the button of 'نوع الإجراء' field ")
            newpopup = al.find("the second 'إضافة - تعديل تسلسل الإجراء' popup")
            newpopup.do("hover on the button of 'نوع الإجراء' field ")
            newpopup.do("click on the button of 'نوع الإجراء' field ")
            newpopup.do(f"type {ActionTypeCode} into 'الرمز' field then press enter from keyboard")
            # newpopup.do("hover on 'بحث' button")
            # newpopup.do("click on 'بحث' button")
            newpopup.do("hover on the first row of the table")
            newpopup.do("click on the first row of the table")
            newpopup.do("hover on 'إختر' button")
            newpopup.do("click on 'إختر' button")

            PopupArea.do("hover on the button of 'من حالة' field ")
            PopupArea.do("click on the button of 'من حالة' field ")
            newpopup = al.find("the second 'إضافة - تعديل تسلسل الإجراء' popup")
            newpopup.do("hover on 'بحث' button")
            newpopup.do("click on 'بحث' button")
            newpopup.do(f"type {FromStatusCode} into 'الرمز' field then press enter from keyboard")
            # newpopup.do("hover on 'بحث' button inside the box")
            # newpopup.do("click on 'بحث' button inside the box")
            res1 = newpopup.get("value under 'الرمز' column")
            assert res1 == FromStatusCode , 'From Status Code result is displayed wrongly'
            newpopup.do("hover on the first row of the table")
            newpopup.do("click on the first row of the table")
            newpopup.do("hover on 'إختر' button")
            newpopup.do("click on 'إختر' button")

            PopupArea.do("hover on the button of 'من منصب' field ")
            PopupArea.do("click on the button of 'من منصب' field ")
            newpopup = al.find("the second 'إضافة - تعديل تسلسل الإجراء' popup")
            newpopup.do("hover on 'بحث' button")
            newpopup.do("click on 'بحث' button")
            newpopup.do(f"type {FromRole} into 'الرمز' field then press enter from keyboard")
            # newpopup.do("hover on 'بحث' button inside the box")
            # newpopup.do("click on 'بحث' button inside the box")
            res2 = newpopup.get("value under 'الإسم' column")
            assert res2 == FromRole , 'From Role result is displayed wrongly'
            newpopup.do("hover on the first row of the table")
            newpopup.do("click on the first row of the table")
            newpopup.do("hover on 'إختر' button")
            newpopup.do("click on 'إختر' button")     

            PopupArea.do("hover on the button of 'إلى حالة' field ")
            PopupArea.do("click on the button of 'إلى حالة' field ")
            newpopup = al.find("the second 'إضافة - تعديل تسلسل الإجراء' popup")
            newpopup.do("hover on 'بحث' button")
            newpopup.do("click on 'بحث' button")
            newpopup.do(f"type {ToStatusCode} into 'الرمز' field then press enter from keyboard")
            # newpopup.do("hover on 'بحث' button inside the box")
            # newpopup.do("click on 'بحث' button inside the box")
            res3 = newpopup.get("value under 'الرمز' column")
            assert res3 == ToStatusCode , 'To Status Code result is displayed wrongly'
            newpopup.do("hover on the first row of the table")
            newpopup.do("click on the first row of the table")
            newpopup.do("hover on 'إختر' button")
            newpopup.do("click on 'إختر' button")  


            PopupArea.do("hover on the button of 'إلى منصب' field ")
            PopupArea.do("click on the button of 'إلى منصب' field ")
            newpopup = al.find("the second 'إضافة - تعديل تسلسل الإجراء' popup")
            newpopup.do("hover on 'بحث' button")
            newpopup.do("click on 'بحث' button")
            newpopup.do(f"type {ToRole} into 'الرمز' field then press enter from keyboard")
            # newpopup.do("hover on 'بحث' button inside the box")
            # newpopup.do("click on 'بحث' button inside the box")
            res4 = newpopup.get("value under 'الإسم' column")
            assert res4 == ToRole , 'To Role result is displayed wrongly'
            newpopup.do("hover on the first row of the table")
            newpopup.do("click on the first row of the table")
            newpopup.do("hover on 'إختر' button")
            newpopup.do("click on 'إختر' button")


            PopupArea.do("hover on the button of 'الحالة الرئيسية' field ")
            PopupArea.do("click on the button of 'الحالة الرئيسية' field ")
            newpopup = al.find("the second 'إضافة - تعديل تسلسل الإجراء' popup")
            newpopup.do("hover on 'بحث' button")
            newpopup.do("click on 'بحث' button")
            newpopup.do(f"type {MainStatusCode} into 'الرمز' field then press enter from keyboard")
            # newpopup.do("hover on 'بحث' button inside the box")
            # newpopup.do("click on 'بحث' button inside the box")
            res5 = newpopup.get("value under 'الرمز' column")
            assert res5 == MainStatusCode , 'Main Status Code result is displayed wrongly'
            newpopup.do("hover on the first row of the table")
            newpopup.do("click on the first row of the table")
            newpopup.do("hover on 'إختر' button")
            newpopup.do("click on 'إختر' button")


            PopupArea.do("hover on 'حفظ' button")

            PopupArea.do(f"hover on {InboxStatus} radio button of 'حالة الصندوق' area")
            PopupArea.do(f"click on {InboxStatus} radio button of 'حالة الصندوق' area")

            PopupArea.do(f"hover on 'نعم' radio button of 'نشط' area")
            PopupArea.do(f"click on 'نعم' radio button of 'نشط' area")

            PopupArea.do("hover on 'حفظ' button")
            PopupArea.do("click on 'حفظ' button")

            print(f"row {i} created successfully")

        except Exception as e:
            print(f'Row {i} failed: {e}')
            continue
        