from screenshot_bot.wordpress import wordpressbot
from screenshot_bot.dolibarr import dolibarrbot
from screenshot_bot.hrsystem import hrsystembot

type = "wp"  # wp(wordpress) / db(dolibarr) / hr
# Wordpress網址 (https://domain.xyz/) HR網址 (https://domain.xyz#/)
domain = "https://jupiter-eyewear.online/"
username = "mgtadmin"  # 登入帳戶
password = "M7TNWKa9LgUGkF5uFEE5x3)X"  # 登入密碼
# 需要截圖的部分，輸入數字並以逗號隔開 e.g. [1,2,3,7,9,10]
parts = [1,2,3,5,6,8,9,10,11]


# ========== WordPress 截圖 Plugin ==========
# 1 公司網站
# 2 網站備份系統
# 3 網站統計系統
# 4 網站安全及防火牆
# 5 銷售單管理系統
# 6 客戶管理系統
# 7 報告管理系統
# 8 公司報表系統
# 9 訂單管理系統
# 10 產品管理系統
# 11 付款管理系統

# ========== HR 截圖 Plugin ==========
# 1 人力資源管理系統
# 2 員工個人資料紀錄 APP支援
# 3 公告板 APP 系統
# 4 GPS 打卡 APP 系統
# 5 編更 APP 系統
# 6 休假 APP 管理系統
# 7 APP用戶管理系統
# 8 費用報銷系統

# ========== Dolibarr 截圖 Plugin ==========
# 1 工作管理系統
# 2 銷售管理系統
# 3 訂單及收據管理系統
# 4 會計系統
# 5 客戶管理系統
# 6 供應商管理系統
# 7 報告管理系統

if type == "wp":
    bot = wordpressbot(domain, username, password, parts)
elif type == "db":
    bot = dolibarrbot(domain, username, password, parts)
elif type == "hr":
    bot = hrsystembot(domain, username, password, parts)
bot.start()

# python3 screenshot.py
