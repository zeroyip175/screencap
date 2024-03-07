from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pyscreenshot as ImageGrab
import os
import traceback
import random


class dolibarrbot:
    # Initialization
    def __init__(self, _domain, _username, _password, _parts):
        global output, domain, username, password, parts, partName, subPartName
        output = "screenshot_bot/output/dolibarr/"
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

    # ===== Start Settings ======
    def startPart(self, name):
        global partName, subPartName
        partName = name
        subPartName = ""
        self.logTitle()  # print the part name for each call
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

    def saveImage(self, x1, y1, x2, y2):
        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        image.save(file_location + subPartName + ".png")

    # CSS (Hide & Highlight)
    def addStyle(self, type, _element, extraStyle=''):
        style = ""
        if type == "hidden":
            pass
            # style = "text-decoration-line: line-through;text-decoration-thickness: 1rem;" + extraStyle
        elif type == "highlight":
            style = "border: 2px solid red;" + extraStyle
        elif type == "custom":
            style = extraStyle
        driver.execute_script(
            "arguments[0].style = '" + style + "';", _element)

    # Switch Pages
    def getPage(self, pageID):
        driver.find_element(By.ID, pageID).click()

    def getRoute(self, queries, subqueries=''):
        mainmenu = ""
        if queries == "companies":  # 合作方/通訊錄
            mainmenu = "societe/index.php?mainmenu=" + queries
        elif queries == "products":  # 產品和服務區域
            mainmenu = "product/index.php?mainmenu=" + queries
        elif queries == "project":  # 專案區域
            mainmenu = "projet/index.php?mainmenu=" + queries
        elif queries == "commercial":  # 銷售|採購區域
            mainmenu = "comm/index.php?mainmenu=" + queries
        elif queries == "billing":  # 帳單和付款區域
            mainmenu = "compta/index.php?mainmenu=" + queries
        elif queries == 'bank':  # 銀行帳戶
            mainmenu = "compta/bank/list.php?mainmenu=" + queries
        elif queries == "home":
            mainmenu = "index.php?mainmenu=home&leftmenu=" + queries
        driver.get(domain + mainmenu)

        if subqueries == "list":  # 潛在客戶電話清單
            mainmenu = "societe/" + subqueries + ".php?type=p"
        elif subqueries == "card":  # 潛在合作方清單
            mainmenu = "societe/" + subqueries + ".php?socid=1"
        driver.get(domain + mainmenu)

    def getMenuItem(self, queriesMenu):
        leftmenu = ""
        if queriesMenu == "thirdparties":  # 合作方清單
            leftmenu = "societe/list.php?leftmenu=" + queriesMenu
        elif queriesMenu == "orders":
            leftmenu = "commande/stats/index.php?leftmenu=" + queriesMenu
        elif queriesMenu == "customers_bills":
            leftmenu = "/compta/facture/list.php?leftmenu=" + queriesMenu
        elif queriesMenu == "tax_various":  # 雜項付款
            leftmenu = "compta/bank/various_payment/list.php?leftmenu=" + queriesMenu
        elif queriesMenu == "checks":
            leftmenu = "compta/paiement/cheque/index.php?leftmenu=" + queriesMenu
        driver.get(domain + leftmenu)

    def setOption(self):
        global options
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("-inprivate")

    # ================ START! ================
    def start(self):
        global options
        options = webdriver.ChromeOptions()
        self.setOption()

        global driver
        try:
            driver = webdriver.Chrome(options=options)
        except:
            options = webdriver.EdgeOptions()
            self.setOption()
            driver = webdriver.Edge(options=options)

        driver.maximize_window()
        driver.implicitly_wait(30)

    # ================ Login ================
        driver.get(domain)
        sleep(1)

        driver.find_element(By.ID, 'username').send_keys(username)
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(
            By.CSS_SELECTOR, 'div#login-submit-wrapper input').click()

        if not os.path.exists(output):
            os.makedirs(output)

    # ================ 1. 工作管理系統 ================
        if 1 in parts:
            try:
                # 1.1 員工界面
                self.startPart("工作管理系統")

                # # 1.1.1 工作管理

                self.startSubPart("工作管理_從上而下的工作分配系統")
                self.getPage("mainmenutd_project")
                driver.get(
                    domain + "projet/activity/perweek.php?leftmenu=tasks")
                sleep(1)
                driver.find_element(By.ID, "select2-taskid-container").click()
                self.saveImage(0, 70, 1920, 600)

                self.startSubPart("工作管理_目前任務進度")
                driver.get(domain + "projet/tasks/list.php?leftmenu=tasks")
                self.saveImage(0, 70, 1920, 480)

                self.startSubPart("工作管理_員工的工作日誌及時間表_工作日誌")
                self.getPage("mainmenutd_agenda")
                driver.get(
                    domain + "comm/action/list.php?mode=show_list&mainmenu=agenda&leftmenu=agenda&idmenu=20")
                self.saveImage(0, 70, 1920, 950)

                self.startSubPart("工作管理_員工的工作日誌及時間表_時間表")
                driver.get(
                    domain + "comm/action/index.php?idmenu=12&mainmenu=agenda&leftmenu=")
                self.saveImage(0, 70, 1920, 950)

                # 1.1.2 任務管理

                self.startSubPart("任務管理_客戶資源分配及編輯")
                self.getPage("mainmenutd_companies")
                driver.find_element(By.ID, "mainmenutd_companies").click()
                elements = driver.find_elements(
                    By.CSS_SELECTOR, "tr.oddeven>td.tdoverflowmax200>a:has(span)")
                for el in elements:
                    self.addStyle("hidden", el)
                dates = driver.find_elements(By.CSS_SELECTOR, "td.tddate")
                for el in dates:
                    self.addStyle("hidden", el)
                sleep(0.8)
                self.saveImage(0, 70, 1920, 760)

                self.startSubPart("任務管理_任務情況一覽及管理")
                self.getPage("mainmenutd_project")
                driver.get(domain + "projet/tasks/list.php?leftmenu=tasks")
                dates = driver.find_elements(
                    By.CSS_SELECTOR, "tr.oddeven>td.center:nth-child(-n+4)")
                for el in dates:
                    self.addStyle("hidden", el)
                self.addStyle("hidden", driver.find_element(
                    By.CSS_SELECTOR, "td.tdoverflowmax150 > a"))
                self.addStyle("hidden", driver.find_element(
                    By.CSS_SELECTOR, "tr.oddeven > td.tdoverflowmax200"))
                sleep(0.8)
                self.saveImage(0, 70, 1920, 480)

                self.startSubPart("任務管理_開展一項新任務_管理任務")
                driver.get(
                    domain + "/projet/tasks/task.php?id=1&withproject=1")
                self.addStyle("hidden", driver.find_element(
                    By.CSS_SELECTOR, "div.refid>div.refidno>a"))
                self.saveImage(0, 70, 1920, 1000)

                self.startSubPart("任務管理_開展一項新任務_管理下線可應用的人力資源")
                self.getPage("mainmenutd_agenda")
                driver.get(
                    domain + "comm/action/peruser.php?mode=show_peruser")
                mission = driver.find_elements(
                    By.CSS_SELECTOR, "td.cal_current_month:not(td.tdoverflowmax100)")
                for el in mission:
                    self.addStyle("custom", el, "background-color:black;")
                sleep(3)
                self.saveImage(0, 70, 1920, 740)

                self.startSubPart("任務管理_開展一項新任務_創建訂單與付款及對應項目")
                self.getPage("mainmenutd_commercial")
                driver.get(
                    domain + "commande/card.php?action=create&leftmenu=orders")
                sleep(1)
                self.saveImage(0, 70, 1920, 920)

                self.startSubPart("任務管理_開展一項新任務_各類工作分配")
                self.getPage("mainmenutd_project")
                driver.get(
                    domain + "projet/tasks.php?leftmenu=tasks&action=create")
                sleep(1)
                self.saveImage(0, 70, 1920, 840)

                self.startSubPart("任務管理_開展一項新任務_跟進工作分配")
                self.getPage("mainmenutd_project")
                driver.get(domain + "projet/list.php?leftmenu=projets")
                driver.find_element(
                    By.ID, "select2-search_project_contact-container").click()
                self.addStyle("highlight", driver.find_element(
                    By.CSS_SELECTOR, "span.select2-dropdown.ui-dialog.select2-dropdown--below"))
                companies = driver.find_elements(
                    By.CSS_SELECTOR, "td.tdoverflowmax200")
                for el in companies:
                    self.addStyle("hidden", el)
                dates = driver.find_elements(
                    By.CSS_SELECTOR, "tr.oddeven > td.center:nth-child(-n+5)")
                for el in dates:
                    self.addStyle("hidden", el)
                sleep(0.5)
                self.saveImage(0, 70, 1920, 585)

                # 1.2 管理界面

                # 1.2.1 工作管理
                self.startSubPart("工作管理_員工工作紀錄_各任務中人力資源分配情況一覽")
                self.getPage("mainmenutd_project")
                driver.get(domain + "/projet/activity/permonth.php")
                self.addStyle("hidden", driver.find_element(
                    By.CSS_SELECTOR, "tr.oddeven a.refurl"))
                self.addStyle("hidden", driver.find_element(
                    By.CSS_SELECTOR, "tr.oddeven span.secondary"))
                self.saveImage(0, 70, 1920, 950)

                self.startSubPart("工作管理_員工工作紀錄")
                self.getPage("mainmenutd_project")
                driver.get(domain + "/projet/tasks/time.php?leftmenu=tasks")
                elements = driver.find_elements(
                    By.CSS_SELECTOR, "tr.oddeven td.nowrap,td.nowraponall:not(td.right,td.center)")
                for el in elements:
                    self.addStyle("hidden", el)
                self.addStyle("hidden", driver.find_element(
                    By.CSS_SELECTOR, "tr.oddeven td.tdoverflowmax100 span.usertext"))
                sleep(1)
                # 1.2.2 人力資源分配總覽

                self.startSubPart("人力資源分配總覽_按任務一覽人力資源投放")
                self.getPage("mainmenutd_agenda")
                driver.get(domain + "comm/action/list.php?mode=show_list")
                contributors = driver.find_elements(
                    By.CSS_SELECTOR, "td.tdoverflowmax150 a:not(.refurl)")
                for el in contributors:
                    self.addStyle("hidden", el)
                dates = driver.find_elements(
                    By.CSS_SELECTOR, "tr.oddeven td.center:nth-child(-n+6)")
                for el in dates:
                    self.addStyle("hidden", el)
                self.saveImage(0, 70, 1920, 950)

                self.startSubPart("人力資源分配總覽_按時間表系統一覽人力資源投放")
                driver.get(
                    domain + "comm/action/index.php?action=default&mainmenu=agenda&leftmenu=agenda&idmenu=15")
                companies = driver.find_elements(
                    By.CSS_SELECTOR, "td.tdoverflow a.refurl")
                for el in companies:
                    self.addStyle("hidden", el)
                calendar = driver.find_elements(
                    By.CSS_SELECTOR, "td.cal_current_month div.tagtr:not(div.cursorpointer,div.tagtd)")
                for el in calendar[random.randrange(4, 10):12]:
                    self.addStyle("custom", el, "background-color:black")
                sleep(3)
                self.saveImage(0, 70, 1920, 950)

            except:
                self.logError()

    # ================ 2. 服務管理系統 ================
        if 2 in parts:
            # 2.1 管理及分配現有客戶帳戶到員工
            try:
                self.startPart("服務管理系統")

                # self.startSubPart("管理及分配現有客戶帳戶到員工")
                # self.getRoute("companies")
                # self.getMenuItem("thirdparties")
                # driver.find_elements(By.CSS_SELECTOR,"tr.oddeven td.tdoverflowmax200 > a")[1].click()
                # try:
                #     driver.find_elements(By.CSS_SELECTOR, "a.butAction")[1].click()
                # except:
                #     driver.find_element(By.CSS_SELECTOR, "a.butAction").click()
                # driver.execute_script("window.scrollBy(0,165);")
                # try:
                #     self.addStyle("hidden",driver.find_element(By.CSS_SELECTOR, "textarea#address"))
                # except:
                #     pass
                # self.addStyle("hidden",driver.find_element(By.ID,"phone"))
                # self.addStyle("hidden",driver.find_element(By.ID,"email"))
                # driver.find_elements(By.CSS_SELECTOR,("ul.select2-selection__rendered"))[2].click()
                # selectedOption = driver.find_elements(By.CSS_SELECTOR, "li.select2-results__option")[0]
                # ActionChains(driver).move_to_element(selectedOption).perform()
                # resultOptions = driver.find_elements(By.CSS_SELECTOR, "li.select2-results__option")
                # for options in resultOptions[1:]:
                #     self.addStyle("hidden",options)
                # driver.execute_script("document.body.style.zoom='70%'")
                # sleep(3)
                # self.saveImage(0, 70, 1920, 950)
            # 2.2 潛在客戶電話跟進及管理系統

                self.startSubPart("潛在客戶電話跟進及管理系統")
                self.getRoute("companies", "list")
                try:
                    prospectList = driver.find_elements(
                        By.CSS_SELECTOR, "td.tdoverflowmax200")
                    for prospect in prospectList:
                        self.addStyle("hidden", prospect)
                    telPhoneList = driver.find_elements(
                        By.CSS_SELECTOR, "span:has(span.fas.fa-phone)")
                    for el in telPhoneList:
                        self.addStyle("hidden", el)
                    sleep(2)
                    self.saveImage(0, 70, 1920, 950)
                except:
                    pass
            # 2.3 各服務之潛在客戶跟進及管理系統
                self.startSubPart("各服務之潛在客戶跟進及管理系統")
                self.getRoute("companies", "card")
                companyInfo = driver.find_element(
                    By.CSS_SELECTOR, "div.refid:has(div.refidno)")
                self.addStyle(
                    "custom", companyInfo, 'text-decoration-line: line-through;text-decoration-thickness: 1rem;color:black;')
                try:
                    url = driver.find_element(
                        By.CSS_SELECTOR, "div.nospan.float > a")
                    self.addStyle(
                        "custom", url, 'text-decoration-line: line-through;text-decoration-thickness: 1rem;color:black;')
                    fb = driver.find_element(
                        By.CSS_SELECTOR, "div.divsocialnetwork:has(a)")
                    self.addStyle(
                        "custom", fb, 'text-decoration-line: line-through;text-decoration-thickness: 1rem;color:black;')
                    self.saveImage(0, 70, 1920, 950)
                except:
                    self.saveImage(0, 70, 1920, 950)
                    pass

             # 2.4 銷售管理情況總覽
                self.startSubPart("銷售管理情況總覽")
                self.getRoute("commercial")
                self.getMenuItem("orders")
                try:
                    elements = driver.find_elements(
                        By.CSS_SELECTOR, "tr.oddeven > td.right")
                    for el in elements:
                        self.addStyle("hidden", el)
                    driver.execute_script("document.body.style.zoom='67%'")
                    self.saveImage(0, 70, 1920, 950)
                except:
                    pass
            # 2.5 銷售及潛在客戶管理系統
                self.startSubPart("銷售及潛在客戶管理系統_員工總覽")
                self.getRoute("commercial")
                driver.get(domain + "/commande/list.php?leftmenu=orders")
                driver.find_element(
                    By.ID, "select2-search_sale-container").click()
                selectedOption = driver.find_elements(
                    By.CSS_SELECTOR, "li.select2-results__option")[1]
                ActionChains(driver).move_to_element(selectedOption).perform()
                resultOptions = driver.find_elements(
                    By.CSS_SELECTOR, "li.select2-results__option")
                for options in resultOptions[2:]:
                    self.addStyle("hidden", options)
                elements = driver.find_elements(
                    By.CSS_SELECTOR, "tr.oddeven > td.center")
                for el in elements[0:]:
                    self.addStyle("hidden", el)
                companies = driver.find_elements(
                    By.CSS_SELECTOR, "tr.oddeven > .tdoverflowmax200 > a.refurl")
                for list in companies:
                    self.addStyle("hidden", list)
                sleep(2)
                self.saveImage(0, 70, 1920, 950)

                self.startSubPart("銷售及潛在客戶管理系統_渠道總覽")
                self.getRoute("")
            # 2.5.1 渠道總覽
                self.startSubPart("銷售及潛在客戶管理系統_渠道總覽")
                self.getRoute("commercial")
                driver.get(domain + "commande/index.php?leftmenu=orders")
                invoices = driver.find_elements(
                    By.CSS_SELECTOR, "td.nowrap > a:has(span)")
                for el in invoices:
                    self.addStyle("hidden", el)
                sleep(2)
                self.saveImage(0, 70, 1920, 950)
            except:
                traceback.print_exc()
                self.logError()
    # ================ 3. 訂單及收據管理系統 ================
        if 3 in parts:
            try:
                self.startPart("訂單及收據管理系統")

            # 3.1新增訂單
                self.startSubPart("新增訂單")
                self.getRoute("commercial")
                driver.get(domain + "commande/list.php?leftmenu=orders")
                elements = driver.find_elements(
                    By.CSS_SELECTOR, "tr.oddeven>td.tdoverflowmax200>a.refurl")
                for el in elements:
                    self.addStyle("hidden", el)
                driver.find_elements(By.CSS_SELECTOR, "tr.oddeven>td.nowrap>input")[
                    0].click()
                edit = driver.find_element(
                    By.CSS_SELECTOR, "div.center > span.select2").click()
                self.addStyle("highlight", driver.find_element(
                    By.CSS_SELECTOR, "span.select2-dropdown"))
                sleep(1)
                self.saveImage(0, 70, 1920, 750)

            # 3.2更改, 刪除訂單
                self.startSubPart("更改, 刪除訂單")
                self.getRoute("billing")
                self.getMenuItem("customers_bills")
                driver.find_elements(By.CSS_SELECTOR, "td.nowraponall >a")[
                    0].click()
                self.addStyle("hidden", driver.find_element(
                    By.CSS_SELECTOR, "div.refid>div.refidno>a.refurl"))
                self.addStyle("hidden", driver.find_element(
                    By.CSS_SELECTOR, "td.linecoldescription:has(a)"))
                self.saveImage(0, 70, 1920, 950)
                sleep(1)

             # 3.3自動生成單據的編號
                self.startSubPart("自動生成單據的編號")
                self.getRoute("billing")
                self.getMenuItem("customers_bills")
                elements = driver.find_elements(
                    By.CSS_SELECTOR, "tr.oddeven>td.tdoverflowmax200>a.refurl")
                for el in elements:
                    self.addStyle("hidden", el)
                invoices = driver.find_elements(
                    By.CSS_SELECTOR, "td.nowraponall:has(tr.nocellnopadd)")
                for el in invoices:
                    self.addStyle("highlight", el)
                self.saveImage(0, 70, 1920, 950)
            # 3.4 搜尋時可按單號和客戶名稱
                self.startSubPart("搜尋時可按單號和客戶名稱")
                self.getRoute("billing")
                self.getMenuItem("customers_bills")
                elements = driver.find_elements(
                    By.CSS_SELECTOR, "tr.oddeven>td.tdoverflowmax200>a.refurl")
                for el in elements:
                    self.addStyle("hidden", el)
                self.addStyle("highlight", driver.find_element(
                    By.CSS_SELECTOR, "tr.liste_titre > [title='參考號']"))
                self.addStyle("highlight", driver.find_element(
                    By.CSS_SELECTOR, "tr.liste_titre > [title='合作方']"))
                self.addStyle("highlight", driver.find_element(
                    By.CSS_SELECTOR, "div.nowraponall> [name='button_search_x']"))
                sleep(1)
                self.saveImage(0, 70, 1920, 950)
            # 3.5 銷售狀況報告
                self.startSubPart("銷售狀況報告")
                self.getRoute("commercial")
                self.getMenuItem("orders")
                elements = driver.find_elements(
                    By.CSS_SELECTOR, "tr.oddeven > td.right")
                for el in elements:
                    self.addStyle("hidden", el)
                sleep(1)
                self.saveImage(0, 70, 1920, 950)
            except:
                self.logError()
                traceback.print_exc()
         # ================ 4. 會計系統 ================
        if 4 in parts:
            # 4.1 一般支收
            try:
                self.startPart("會計系統")
                self.startSubPart("一般支收")
                self.getRoute("billing")
                self.getMenuItem("tax_various")
                driver.find_element(
                    By.CSS_SELECTOR, "li.paginationafterarrows > a").click()
                sleep(1)
                self.saveImage(0, 70, 1920, 950)

            # 4.2 交易記錄|未配對交易|已配對交易|所有交易
                self.startSubPart("交易記錄|未配對交易|已配對交易|所有交易")
                self.getRoute("bank")
                driver.find_element(
                    By.CSS_SELECTOR, "td.nowraponall > a").click()
                driver.find_element(By.CSS_SELECTOR, "a#journal").click()
                elements = driver.find_elements(
                    By.CSS_SELECTOR, "tr.oddeven > td.nowrap")
                for el in elements[1:]:
                    self.addStyle("hidden", el)
                self.saveImage(0, 70, 1920, 950)
                sleep(3)

            # 4.3 支票交易配對|其他收入|其他開銷
                self.startSubPart("支票交易配對|其他收入|其他開銷")
                self.getRoute("bank")
                self.getMenuItem("checks")
                self.addStyle("highlight", driver.find_element(
                    By.CSS_SELECTOR, "div.fichethirdleft > table"))
                self.addStyle("hidden", driver.find_element(
                    By.CSS_SELECTOR, "div.fichetwothirdright tr.oddeven> td:not(td.right,td.nowraponall)"))
                self.addStyle("hidden", driver.find_element(
                    By.CSS_SELECTOR, "div.fichetwothirdright tr.oddeven > td.right:has(span.amount)"))
                self.saveImage(0, 70, 1920, 950)

                self.startSubPart("支票交易配對|其他收入|其他開銷_2")
                try:
                    driver.find_element(
                        By.CSS_SELECTOR, "tr.oddeven > td.nowraponall > a").click()
                    self.addStyle("hidden", driver.find_element(
                        By.CSS_SELECTOR, "table.border > tbody > tr >td:not(td.titlefield)"))
                    elements = driver.find_elements(
                        By.CSS_SELECTOR, "table.border > tbody >tr >td[colspan]")
                    for el in elements:
                        self.addStyle("hidden", el)
                    self.addStyle("hidden", driver.find_element(
                        By.CSS_SELECTOR, "tr.oddeven >td:not(td.right,td.center)"))
                    self.addStyle("hidden", driver.find_element(
                        By.CSS_SELECTOR, "tr.oddeven > td.right:has(span.amount)"))
                    self.addStyle("hidden", driver.find_element(
                        By.CSS_SELECTOR, "td.center:nth-child(-2n+2)"))
                    self.saveImage(0, 70, 1920, 950)
                except:
                    pass
                sleep(3)
            except:
                self.logError
                traceback.print_exc()
        # ================ 5. 客戶管理系統 ================
        if 5 in parts:
            # 5.1 記錄客戶資料|自動記錄客戶購買資訊
            try:
                self.startPart("客戶管理系統")
                self.startSubPart("記錄客戶資料|自動記錄客戶購買資訊")
                self.getRoute("companies")
                self.getMenuItem("thirdparties")

                elements = driver.find_elements(
                    By.CSS_SELECTOR, "tr.oddeven >td.tdoverflowmax200>a:has(span)")
                for el in elements:
                    self.addStyle("hidden", el)
                phoneNumbers = driver.find_elements(
                    By.CSS_SELECTOR, "td.nowraponall > span:has([title='電話'])")
                for phones in phoneNumbers:
                    self.addStyle("hidden", phones)
                self.saveImage(0, 70, 1920, 950)
                sleep(2)
            # 5.2 客戶過往購買紀錄
                self.startSubPart("客戶過往購買紀錄")
                self.getRoute("companies", "list")
                try:
                    driver.find_elements(By.CSS_SELECTOR, "tr.oddeven>td>a")[
                        0].click()
                    driver.get(domain+"comm/card.php?socid=1")
                    self.addStyle("hidden", driver.find_element(
                        By.CSS_SELECTOR, "div.refid"))
                    price = driver.find_elements(
                        By.CSS_SELECTOR, "div.boxstats > span.boxstatsindicator")
                    for el in price:
                        self.addStyle("hidden", el)
                    sleep(2)
                    info = driver.find_elements(
                        By.CSS_SELECTOR, "tr.oddeven > td.right:nth-child(-n+3)")
                    for el in info:
                        self.addStyle("hidden", el)
                    self.addStyle("highlight", driver.find_element(
                        By.CSS_SELECTOR, "div.fichehalfright"))
                    sleep(2)
                    self.saveImage(0, 70, 1920, 950)
                except:
                    pass
            # 5.3 搜尋客戶資料時可按客戶名稱/電話查詢
                self.startSubPart("搜尋客戶資料時可按客戶名稱_電話查詢")
                self.getRoute("third-parties", "card")
                self.addStyle("hidden", driver.find_element(
                    By.CSS_SELECTOR, "div.refid"))
                self.addStyle("hidden", driver.find_element(
                    By.CSS_SELECTOR, "table.tableforfield>tbody>tr>td[colspan]>a>span.usertext"))
                staff = driver.find_elements(
                    By.CSS_SELECTOR, "td.tdoverflowmax125")
                for el in staff:
                    self.addStyle("hidden", el)
                driver.execute_script("document.body.style.zoom='67%'")
                self.saveImage(0, 70, 1920, 950)
                sleep(5)
            except:
                self.logError
                traceback.print_exc()
        # ================ 6. 供應商管理系統 ================
        if 6 in parts:
            try:
                self.startPart("供應商管理系統")
            # Defualt id=1 is the administrator, id=2 is the manager, and id>=3 are the employees
            # 6.1 供應商報告層次
                self.startSubPart("供應商報告層次")
                self.getRoute("companies")
                driver.get(domain + "fourn/card.php?socid=2")
                self.addStyle("hidden", driver.find_element(
                    By.CSS_SELECTOR, "div.arearef div.refid"))
                elements = driver.find_elements(
                    By.CSS_SELECTOR, "div.boxstats .boxstatsindicator")
                for el in elements:
                    self.addStyle("hidden", el)
                sleep(1)
                self.saveImage(0, 70, 1920, 950)
            # 6.2 供應商報告訂單
                self.startSubPart("供應商報告訂單")
                self.getRoute("commercial")
                driver.get(domain + "supplier_proposal/card.php?id=1")
                self.addStyle("hidden", driver.find_element(
                    By.CSS_SELECTOR, "div.refidno a.refurl"))
                self.addStyle("hidden", driver.find_element(
                    By.CSS_SELECTOR, "tr[data-element='supplier_proposaldet'] a"))
                sleep(2)
                self.saveImage(0, 70, 1920, 950)
            # 6.3 供應商資料儲存
                self.startSubPart("供應商資料儲存")
                self.getRoute("companies")
                driver.get(domain + "societe/list.php?type=f")
                prospects = driver.find_elements(
                    By.CSS_SELECTOR, "tr.oddeven a.refurl")
                for el in prospects:
                    self.addStyle("hidden", el)
                telPhoneList = driver.find_elements(
                    By.CSS_SELECTOR, "td.nowraponall span:has(span.fa-phone)")
                for phones in telPhoneList:
                    self.addStyle("hidden", phones)
                self.saveImage(0, 70, 1920, 950)
            # 6.4 搜尋供應商資料時可按供應商名稱/電話查詢
                self.startSubPart("搜尋供應商資料時可按供應商名稱_電話查詢")
                self.getRoute("companies")
                driver.get(domain + "societe/card.php?socid=1")
                driver.find_element(
                    By.CSS_SELECTOR, "span.select2-selection.select2-selection--single.searchselectcombo.vmenusearchselectcombo").click()
                search = driver.find_element(
                    By.CSS_SELECTOR, "span.select2-search input.select2-search__field")
                self.addStyle("hidden", driver.find_element(
                    By.CSS_SELECTOR, "div.refid"))
                names = driver.find_elements(
                    By.CSS_SELECTOR, "tr.oddeven td.tdoverflowmax125")
                for el in names:
                    self.addStyle("hidden", el)
                dates = driver.find_elements(
                    By.CSS_SELECTOR, "tr.oddeven td.nowraponall:nth-child(n+3)")
                for el in dates:
                    self.addStyle("hidden", el)
                driver.execute_script("document.body.style.zoom='67%'")
                search.send_keys("1")
                self.addStyle("hidden", search)
                sleep(2)
                self.saveImage(0, 70, 1920, 950)
            # 6.5 數據備份
                # uploaded in output folder
            except:
                self.logError()
                traceback.print_exc()
    # ================ 7. 報告管理系統 ================
        if 7 in parts:
            try:
                self.startPart("報告管理系統")
            # Defualt id=1 is the administrator, id=2 is the manager, and id>=3 are the employees
            # 7.1 員工報告層次
                self.startSubPart("員工報告層次")
                self.getRoute("home")
                driver.get(domain + "user/card.php?id=3&leftmenu=users")
                names = driver.find_element(By.CSS_SELECTOR, "div.refid")
                loginName = driver.find_element(
                    By.CSS_SELECTOR, "span.clipboardCPValue")
                self.addStyle("hidden", loginName)
                self.addStyle("hidden", names)
                sleep(2)
                self.saveImage(0, 70, 1920, 950)
            # 7.2 經理報告層次
                self.startSubPart("經理報告層次")
                driver.get(domain + "user/card.php?id=2&leftmenu=users")
                self.saveImage(0, 70, 1920, 950)
            # 7.3 員工的訪問權限
                self.startSubPart("員工的訪問權限")
                driver.get(domain + "user/perms.php?id=3")
                names = driver.find_element(By.CSS_SELECTOR, "div.refid")
                loginName = driver.find_element(
                    By.CSS_SELECTOR, "span.clipboardCPValue")
                self.addStyle("hidden", loginName)
                self.addStyle("hidden", names)
                self.saveImage(0, 70, 1920, 950)
            except:
                self.logError()
                traceback.print_exc()
