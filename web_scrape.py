
#This program scraps data from amazon and stores into excel and mysql databases.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import xlwt 
import mysql.connector
from xlwt import Workbook 
wb = Workbook() 
sheet1 = wb.add_sheet('Sheet 1')
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
browser = webdriver.Chrome(executable_path='/home/mukesh/Desktop/backup/Programminghub/whatsapp_python_scripts/chromedriver_linux64/chromedriver', chrome_options=option)
browser.get("https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=macbook")
timeout = 0
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@class='s-access-image cfMarker']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()
titles_element = browser.find_elements_by_xpath("//div[@class='s-item-container']")
titles = []
for x in titles_element:
    value=x.text
    value=value.encode('ascii', 'ignore')
    titles.append(value)
def find_nth(s, x, n):
    i = -1
    for _ in range(n):
        i = s.find(x, i + len(x))
        if i == -1:
            break
    return i
checksy=[] #names 
pricey=[] #prices
p1,p2,p3,p4=[],[],[],[] # 4 parameters at side
#Don't go by below logic,it's pathetic. I won't understand after a month myself forget others.
for i in xrange(0,len(titles)):
 if("Sponsored" not in titles[i]):
  try:
   check=titles[i]
   index=check.index('\n')
   check1=check[:index]
   checksy.append(check1)
   check=titles[i]
   pos=find_nth(check,'\n',2)
   check=check[pos+1:]
   index1=find_nth(check,' ',3)
   index2=find_nth(check,'\n',1)
   if(index2<index1):
    index=index2
   else:
    index=index1
   price=check[:index]
   if("used" in price):
     index=price.index('u')
   if("new" in price ):
     index=price.index('n')
   price=price[:index]
   pricey.append(price)
   word='Cpu'
   check1=check
   r=re.compile(r'\b%s\b' % word, re.I)
   m = r.search(check1)
   start=m.start()
   check1=check1[start:]
   index2=find_nth(check1,'\n',1)
   check1=check1[:index2]
   p1.append(check1)
   word='Display'
   r=re.compile(r'\b%s\b' % word, re.I)
   m = r.search(check)
   start=m.start()
   check2=check[start:]
   index2=find_nth(check2,'\n',1)
   check2=check2[:index2]
   p2.append(check2)
   word='Operating'
   r=re.compile(r'\b%s\b' % word, re.I)
   m = r.search(check)
   start=m.start()
   check3=check[start:]
   index3=find_nth(check3,'\n',1)
   check3=check3[:index3]
   p3.append(check3)
   word='Computer'
   r=re.compile(r'\b%s\b' % word, re.I)
   m = r.search(check)
   start=m.start()
   check4=check[start:]
   index4=find_nth(check4,'\n',1)
   check4=check4[:index4]
   p4.append(check4)
  except:
    break
#writing in example.xls a excel file
'''for i in xrange(0,len(pricey)):
  sheet1.write(i,0,checksy[i])
  sheet1.write(i,1,pricey[i][2:])
  sheet1.write(i,2,p1[i][17:])
  sheet1.write(i,3,p2[i][13:])
  sheet1.write(i,4,p3[i][17:])
  sheet1.write(i,5,p4[i][20:])
wb.save('/home/mukesh/Desktop/Scrapping/example.xls')
'''
#writing into database:
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="scraping"
)
mycursor = mydb.cursor()
for i in xrange(0,len(pricey)):
  sql = "INSERT INTO amazon (Name,Price,Cpu_Model,Display_size,Operating_System,Ram_Size) VALUES (%s, %s, %s, %s, %s, %s)"
  val = (checksy[i],pricey[i][2:],p1[i][17:],p2[i][13:],p3[i][17:],p4[i][21:])
  mycursor.execute(sql, val)
  mydb.commit()
print("Done")