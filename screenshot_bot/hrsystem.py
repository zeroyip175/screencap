from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pyscreenshot as ImageGrab
import os
from urllib.parse import urlparse
import traceback


class hrsystembot:
    def __init__(self, _domain, _username, _password, _parts):
        global output, domain, username, password, parts, partName, subPartName
        output = "screenshot_bot/output/hr/"
        domain = _domain
        username = _username
        password = _password
        parts = _parts
        partName = ""
        subPartName = ""

    def logTitle(self):
        print("開始擷取 [" + partName + "] " + subPartName)

    def logError(self):
        print("========= 發生錯誤 =========")

    def startPart(self, name):
        global partName, subPartName
        partName = name
        subPartName = ""
        self.logTitle()
        self.setFileLocation(name)

    def startSubPart(self, name):
        global subPartName
        subPartName = name
        self.logTitle()

    def setFileLocation(self, name):
        global file_location
        file_location = output + name + "/"
        if not os.path.exists(file_location):
            os.makedirs(file_location)

    # Crop the area of the image
    # x1,y1: url path area | x2,y2: rest of the screen area
    def saveImage(self, x1, y1, x2, y2):
        image = ImageGrab.grab(bbox=(x1, y1, x2, y2+70))
        image.save(file_location + subPartName + ".png")

    def addStyle(self, type, _element, extraStyle=''):
        style = ""
        if type == "hidden":
            style = "text-decoration-line: line-through;text-decoration-thickness: 1rem;" + extraStyle
        elif type == 'hidden-bg':
            style = "background-image: linear-gradient(to left, currentColor 80%, transparent 30%);" + extraStyle
        elif type == "highlight":
            style = "border: 2px solid red;" + extraStyle
        elif type == "custom":
            style = extraStyle
        driver.execute_script(
            "arguments[0].style = '" + style + "';", _element)

    def setOption(self):
        global options
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)

    def getPath(self, url):
        parsed_url = urlparse(url)

    def start(self):
        global options
        options = webdriver.ChromeOptions()
        self.setOption()
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("-inprivate")

        global driver
        try:
            driver = webdriver.Chrome(options=options)
        except:
            options = webdriver.EdgeOptions()
            self.setOption()
            driver = webdriver.Edge(options=options)

        driver.maximize_window()
        driver.implicitly_wait(30)

    # ====== Login =======
        driver.get(domain)
        sleep(1)

        driver.find_element(By.ID, "email-address").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.CLASS_NAME, 'login').click()
        sleep(3)

        if not os.path.exists(output):
            os.makedirs(output)

        # 1. 人力資源管理系統
        if 1 in parts:
            try:
                # 1.1 員工資料
                self.startPart("人力資源管理系統")

                self.startSubPart("員工資料")
                employeesPath = 'employees'
                driver.get(domain + employeesPath)
                sleep(3)
                employees = driver.find_elements(
                    By.CSS_SELECTOR, "tr.el-table__row div:nth-child(2):not(.el-popconfirm__action) span")
                for el in employees:
                    self.addStyle(
                        "custom", el, 'background-image:linear-gradient(to left, currentColor 62%, transparent 30%);')
                emails = driver.find_elements(
                    By.CSS_SELECTOR, "tr.el-table__row td:nth-child(2) span")
                for el in emails:
                    self.addStyle(
                        "custom", el, 'background-image:linear-gradient(to left, currentColor 62%, transparent 30%);')
                phones = driver.find_elements(
                    By.CSS_SELECTOR, "tr.el-table__row td:nth-child(3) span")
                for el in phones:
                    self.addStyle(
                        "custom", el, 'background-image:linear-gradient(to left, currentColor 62%, transparent 30%);')
                dates = driver.find_elements(
                    By.CSS_SELECTOR, "tr.el-table__row td:nth-child(4) span")
                for el in dates:
                    self.addStyle(
                        "custom", el, 'background-image:linear-gradient(to left, currentColor 62%, transparent 30%);')
                # driver.find_element(By.ID, "hideTableInfo").click()
                driver.find_element(By.ID, 'hide').click()
                self.saveImage(0, 70, 1920, 760)

                # 1.2 管理級別員工
                self.startSubPart("管理級別員工")
                deptPath = 'departments'
                driver.get(domain + deptPath)
                sleep(1)
                driver.find_elements(
                    By.CSS_SELECTOR, "div.el-table__fixed-right button.viewDept")[0].click()
                sleep(1)
                self.addStyle("custom", driver.find_element(By.CSS_SELECTOR, "div.manager input.el-input__inner"),
                              'background-image: linear-gradient(to left, currentColor 97%, transparent 14%);')
                sleep(3)
                elements = driver.find_elements(
                    By.CSS_SELECTOR, "span.el-checkbox__label span:first-child")
                for el in elements:
                    self.addStyle("hidden-bg", el)
                self.saveImage(0, 70, 1920, 753)
            except:
                self.logError()

        # 2. 員工個人資料紀錄 APP支援
        if 2 in parts:
            try:
                # 2.1統一紀錄員工資料
                self.startPart('員工個人資料紀錄_APP支援')

                self.startSubPart('統一紀錄員工資料')
                employeesPath = 'employees'
                driver.get(domain + employeesPath)
                sleep(3)
                driver.find_element(By.ID, "hideTableInfo").click()
                driver.find_element(By.ID, 'hide').click()
                self.saveImage(0, 70, 1920, 760)

                # 2.2姓名/所屬部門/職位

                self.startSubPart('姓名_所屬部門_職位')
                driver.find_elements(
                    By.CSS_SELECTOR, "tr.el-table__row button.el-button--info.is-plain")[0].click()
                # driver.find_elements(By.ID, "hide")[0].click()
                driver.find_element(
                    By.CSS_SELECTOR, "button.el-button.el-button--primary").click()
                driver.find_element(
                    By.CSS_SELECTOR, "button.el-button.el-button--danger").click()
                sleep(2)
                self.saveImage(0, 70, 1920, 950)
            except:
                traceback.print_exc()
                self.logError()
        # 3. 公告板 APP 系統
        if 3 in parts:
            try:
                # 3.1 管理員可向全公司發送自訂公告
                self.startPart('公告板APP系統')

                self.startSubPart('管理員可向全公司發送自訂公告')
                notifyPath = 'notification'
                driver.get(domain + notifyPath)
                driver.find_element(
                    By.CSS_SELECTOR, "button.notifyBtn").click()
                sleep(1)
                driver.find_elements(
                    By.CSS_SELECTOR, "div.el-switch")[0].click()
                sleep(0.5)
                self.saveImage(0, 70, 1920, 890)
            except:
                traceback.print_exc()
                self.logError()
        # 4 GPS打卡APP 系統
        if 4 in parts:
            try:

                # 4.1 管理員可以檢視所有員工打卡紀錄
                self.startPart('GPS打卡APP系統')

                self.startSubPart('出勤記錄')
                attendencePath = 'attendance'
                driver.get(domain + attendencePath)
                sleep(2)
                driver.find_element(
                    By.CSS_SELECTOR, "button:has(.el-icon-caret-left)").click()
                sleep(1)
                driver.find_element(By.ID, "update-record-btn").click()
                sleep(1)
                names = driver.find_elements(
                    By.CSS_SELECTOR, "div[name='empName'] div")
                for el in names:
                    self.addStyle("hidden-bg", el)
                driver.find_elements(By.CSS_SELECTOR, ".el-button")[0].click()
                sleep(2)
                self.saveImage(0, 70, 1920, 890)

                self.startSubPart('公司位置_打卡範圍')
                gpsPath = 'setting'
                driver.get(domain + gpsPath)
                sleep(1)
                self.saveImage(0, 70, 1920, 890)
            except:
                traceback.print_exc()
                self.logError()

        # 5 編更APP系統
        if 5 in parts:
            try:
                self.startPart('編更APP系統')

                self.startSubPart('更改_編制上班及下班時間')
                rosterPath = 'roster'
                driver.get(domain + rosterPath)
                sleep(3)
                self.saveImage(0, 70, 1920, 890)

                self.startSubPart('當日上班下班時間')
                shiftPath = 'shift'
                driver.get(domain + shiftPath)
                sleep(1)
                self.saveImage(0, 70, 1920, 890)
            except:
                self.logError()

        # 6 休假APP管理系統
        if 6 in parts:
            try:
                self.startPart('休假APP管理系統')

                self.startSubPart('管理員批核申請_1')
                leavePath = 'leave'
                driver.get(domain + leavePath)
                sleep(2)
                self.saveImage(0, 70, 1920, 890)

                self.startSubPart('管理員批核申請_2')
                driver.find_elements(By.CSS_SELECTOR, "button.leaveEditBtn")[
                    0].click()
                sleep(2)
                self.saveImage(0, 70, 1920, 890)

            except:
                self.logError()

        # 7 APP用戶管理系統
        if 7 in parts:
            try:
                self.startPart('APP用戶管理系統')

                self.startSubPart('踢除用戶')
                employeesPath = 'employees'
                driver.get(domain + employeesPath)
                driver.find_element(By.ID, "hideTableInfo").click()
                driver.find_element(By.ID, 'hide').click()
                sleep(2)
                driver.find_elements(By.CSS_SELECTOR, "button.employeeDeleteBtn")[
                    0].click()
                sleep(3)
                self.saveImage(0, 70, 1920, 890)

                self.startSubPart('提供QRCODE')
                driver.find_element(
                    By.CSS_SELECTOR, 'button.addEmployeeBtn').click()
                sleep(2)
                self.saveImage(0, 70, 1920, 890)

            except:
                self.logError()

        # 8 費用報銷系統
        if 8 in parts:
            try:
                self.startPart('費用報銷系統')

                self.startSubPart('記錄報銷的資料')
                claimPath = 'claim'
                driver.get(domain + claimPath)
                sleep(1)
                self.saveImage(0, 70, 1920, 890)
            except:
                self.logError()
