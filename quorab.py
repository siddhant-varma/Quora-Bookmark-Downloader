from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pyperclip
import pdfkit
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.webdriver.common.action_chains import ActionChains
import tkinter as tk

creds={}
username = ''
password = ''


def save_credential(field=0):
    global username
    global password
    if field == 1:
        username = str(input("Enter username/email for Quora Account:"))
    elif field == 2:
        password = str(input("Enter password for Quora Account:"))
    else:
        username = str(input("Enter username/email for Quora Account:"))
        password = str(input("Enter password for Quora Account:"))
    with open("creds.dat",'w') as cred:
        cred.write("quora:%s-%s" %(username, password))
    open_credential()

#Extracts all the credantials from the file
def open_credential():
    global username
    global password
    try:
        with open("creds.dat",'r') as cred:
            for line in cred:
                username = line.split(':')[1].strip().split('-')[0]
                password = line.split(':')[1].strip().split('-')[1]
                creds[line.split(':')[0]]= [username,password]
    except FileNotFoundError:
        save_credential()


open_credential()


#Disable Infobar on Chrome automated web browser
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
brow = webdriver.Chrome(chrome_options=chrome_options)


brow.get("https://www.quora.com/bookmarked_answers")
brow.find_element_by_xpath('//*[@class="text header_login_text_box ignore_interaction"]').send_keys(creds['quora'][0])
brow.find_element_by_xpath('//*[@placeholder="Password"]').send_keys(creds['quora'][1])
time.sleep(1)
brow.find_element_by_xpath('//*[@value="Login"]').click()
time.sleep(1)

first_question=brow.find_element_by_class_name("question_link").text
brow.get("https://www.quora.com/bookmarked_answers?order=desc")

#wait_inp=input("\n\n\t\tPress Enter after Bookmark page is Fully Loaded\n\n")

i=0
while True:
	brow.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	currentQuestion=brow.find_elements_by_class_name("question_link")
	currentQuestion=currentQuestion[len(currentQuestion)-1].text
	i+=1
	if(first_question == currentQuestion):
		break


brow.execute_script("window.scrollTo(0, 0);")
time.sleep(1)
#elem_share=brow.find_elements_by_link_text("Share")
t=tk.Tk()
"""g = brow.find_element_by_class_name('icon_svg-stroke')
actions = ActionChains(brow)
actions.move_to_element(g).click().perform()"""
a=brow.find_elements_by_class_name('AnswerQuickShare')
links=[]
print("HERE")
time.sleep(2)
for i in range(246,len(a),2):
    try:
        ActionChains(brow).move_to_element(a[i]).click().perform()
        time.sleep(2)
        l=brow.find_element_by_link_text('Copy Link')
        ActionChains(brow).move_to_element(l).click().perform()
        time.sleep(1)
        text = t.clipboard_get()
        print(text)
        links.append(text)
    except selenium.common.exceptions.StaleElementReferenceException:
        print("Stale Element Exception Caught for i=%i" %i)



"""ActionChains(brow).move_to_element(brow.find_element_by_class_name('AnswerQuickShare')).click().perform()
time.sleep(1)
l=brow.find_element_by_link_text('Copy Link')
ActionChains(brow).move_to_element(l).click().perform()
time.sleep(1)
text = tk.Tk().clipboard_get()
"""



"""#open tab
brow.find_element_by_tag_name('body').send_keys(Keys.LEFT_CONTROL + 't') 

# Load a page 
brow.get(text)
# Make the tests...
input()
# close the tab
brow.find_element_by_tag_name('body').send_keys(Keys.LEFT_CONTROL + 'w') 
#brow.close()
"""
options = {
	'page-size': 'Letter',
	'dpi': 450,
	'javascript-delay':10000
}
soup=BeautifulSoup(brow.page_source,"lxml")
#div = soup.find_all("div", {"class" : "feed_item inline_expand_item"})
#ques = soup.find_all("a", { "class" : "question_link" })
#q_text = '//*[@id="__w2_oruv77R_link"]/span/span'
#pdfkit.from_string(brow.page_source,brow.title+'.pdf',options=options)
"""
for each in div:
        print("HERE")
        #q = each.span.span.div.div.div.a.text
        #print(q)
        for texts in each.find_all("span", {"class" : "ui_qtext_rendered_qtext"}):
                print(texts.text)
        #print(ans)
"""
"""l=len(elem_share)
j=0
for i in range(l):
	try:
		elem_share[i].click()
		time.sleep(3)
		elem_copy=brow.find_element_by_link_text("Copy Link")
		elem_copy.click()
		ans_url=pyperclip.paste()
		conn=urlopen(ans_url)
		soup = BeautifulSoup(conn.read(),"html.parser")
		title=soup.find('a',class_="question_link").text
		pdfkit.from_url(ans_url,title+'.pdf',options=options)
	except:
		j+=1
		print("Fail",j)
"""	
print("Conversion Completed")


def write_file(links):
    with open(file+".sid",'a+') as out:
        for link in links:
            out.write(link+"\n")




