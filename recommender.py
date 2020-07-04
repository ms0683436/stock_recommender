from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import threading

# 投信連買
def get_trust_always_buy_all(page_source):
    page = BeautifulSoup(page_source, 'html.parser')
    stock_list = page.find('table', id='tblStockList')
    recommand = []
    for stock in stock_list.tbody.find_all('tr')[:50]:
        can_add = True
        stock_detail = stock.find_all('td')
        for stock_buy in stock_detail[7:15]:
            net_buy = stock_buy.nobr.a.get_text()
            net_buy = float(net_buy[:len(net_buy)-1])
            if net_buy < 0:
                can_add = False
                break
        
        if can_add:
            recommand.append(stock_detail[1].nobr.a.get_text())

    return recommand

def set_browser():
    opts = Options()
    ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
    opts.add_argument("user-agent={}".format(ua))  # 使用偽造的 user-agent
    # 使用chrome的webdriver
    return webdriver.Chrome("chromedriver.exe")

def service(stock_id):
    if (validate(stock_id)):
        print('--'+stock_id+'--')

def validate(stock_id):
    return share_capital(stock_id) and shareholder_sturcture(stock_id) 

def share_capital(stock_id):
    share_capital_url = 'https://www.cnyes.com/twstock/intro/' + stock_id + '.htm'
    browser.get(share_capital_url)
    source = browser.page_source
    return check_share_capital(source)

# 去掉股本太大的公司
def check_share_capital(page_source):
    page = BeautifulSoup(page_source, 'html.parser')
    stock_detail = page.find('span', id='ctl00_ContentPlaceHolder1_Label015')
    share_capital = strToFloat(stock_detail.get_text())

    return share_capital < 10000000000

def shareholder_sturcture(stock_id):
    shareholder_structure_url = 'https://norway.twsthr.info/StockHolders.aspx?stock=' + stock_id
    browser.get(shareholder_structure_url)
    source = browser.page_source
    return check_shareholder_sturcture(source)


def strToFloat(number):
    str_number = number.split(',')

    value = ''
    for str_num in str_number:
        value += str_num

    return float(value)

# 大戶持股比例上升
def check_shareholder_sturcture(page_source):
    page = BeautifulSoup(page_source, 'html.parser')
    stock_list = page.find('table', id='Details')
    
    details = stock_list.tbody.find_all('tr')
    previous_total_people = strToFloat(details[1].find_all('td')[4].get_text())
    previous_avg_per_person = strToFloat(details[1].find_all('td')[5].get_text())
    previous_hundreds_stock = strToFloat(details[1].find_all('td')[7].get_text())
    
    can_buy = True
    for detail in details[3:8:2]:
        stock_detail = detail.find_all('td')
        total_people = strToFloat(stock_detail[4].get_text())
        avg_per_person = strToFloat(stock_detail[5].get_text())
        hundreds_stock_percent = strToFloat(stock_detail[7].get_text())

        if previous_total_people > total_people:
            can_buy = False
            break
        
        if previous_avg_per_person < avg_per_person:
            can_buy = False
            break

        if previous_hundreds_stock < hundreds_stock_percent:
            can_buy = False
            break

    return can_buy
    
# Todo
# 判斷是否多頭
def long():
    shareholder_structure_url = 'https://www.wantgoo.com/stock/astock/techchart?stockno=' + stock_id
    browser.get(shareholder_structure_url)
    source = browser.page_source
    return check_long(source)


browser = set_browser()

trust_buy_url = 'https://goodinfo.tw/StockInfo/StockList.asp?RPT_TIME=&MARKET_CAT=%E7%86%B1%E9%96%80%E6%8E%92%E8%A1%8C&INDUSTRY_CAT=%E6%8A%95%E4%BF%A1%E8%B2%B7%E8%B6%85%E4%BD%94%E7%99%BC%E8%A1%8C%E5%BC%B5%E6%95%B8+%E2%80%93+%E4%B8%89%E5%80%8B%E6%9C%88%40%40%E6%8A%95%E4%BF%A1%E8%B2%B7%E8%B6%85%E4%BD%94%E7%99%BC%E8%A1%8C%E5%BC%B5%E6%95%B8%40%40%E6%8A%95%E4%BF%A1+%E2%80%93+%E4%B8%89%E5%80%8B%E6%9C%88&SHEET=%E6%B3%95%E4%BA%BA%E8%B2%B7%E8%B3%A3%E7%B5%B1%E8%A8%88%5F%E6%8A%95%E4%BF%A1&SHEET2=%E8%B2%B7%E8%B3%A3%E8%B6%85%E4%BD%94%E7%99%BC%E8%A1%8C%E5%BC%B5%E6%95%B8&RPT_TIME=%E6%9C%80%E6%96%B0%E8%B3%87%E6%96%99'

browser.get(trust_buy_url)

source = browser.page_source
recommand = get_trust_always_buy_all(source)

t_list=[]
print(recommand)
# Todo
# for stock_id in recommand:
#     service(stock_id)
    # t_list.append(threading.Thread(target=service,args=(stock_id,)))


# for t in t_list:
#     t.start()

browser.close()
