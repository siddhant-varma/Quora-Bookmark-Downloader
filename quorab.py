from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pyperclip
import pdfkit
import os
import selenium.common.exceptions
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.webdriver.common.action_chains import ActionChains
import tkinter as tk

creds={}
links=[]
username = ''
password = ''
delimiter="~"
options = {
	'page-size': 'Letter',
	'dpi': 450,
	'javascript-delay':10000
}
def write_file(links,file):
    with open(file+".sid",'a+') as out:
        for link in links:
            out.write(link+"\n")


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
        cred.write("quora:%s%s%s" %(username, delimiter, password))
    open_credential()

#Extracts all the credantials from the file
def open_credential():
    global username
    global password
    try:
        with open("creds.dat",'r') as cred:
            for line in cred:
                username = line.split(':')[1].strip().split(delimiter)[0]
                password = line.split(':')[1].strip().split(delimiter)[1]
                creds[line.split(':')[0]]= [username, password]
    except FileNotFoundError:
        save_credential()

def Login():
    global brow
    brow.get("https://www.quora.com/bookmarked_answers")
    brow.find_element_by_xpath('//*[@class="text header_login_text_box ignore_interaction"]').send_keys(creds['quora'][0])
    brow.find_element_by_xpath('//*[@placeholder="Password"]').send_keys(creds['quora'][1])
    time.sleep(1)
    brow.find_element_by_xpath('//*[@value="Login"]').click()
    time.sleep(1)

def expand_page():
    global brow
    first_question=brow.find_element_by_class_name("question_link").text
    brow.get("https://www.quora.com/bookmarked_answers?order=desc")

    i=0
    while True:
            brow.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            currentQuestion=brow.find_elements_by_class_name("question_link")
            currentQuestion=currentQuestion[len(currentQuestion)-1].text
            i+=1
            if(first_question == currentQuestion):
                    break


    brow.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

restricted_chars=['/',"\\","*",":","?","<",">","|",'"',"."]

def save_answer(link,serial):
    global brow
    brow.get(link)
    #implement a method to check page loaded or not
    if not os.path.exists(os.getcwd()+"\\pdf\\"):
        os.makedirs(os.getcwd()+"\\pdf\\")
    writer=brow.title[:brow.title.find("'s")]
    writer=writer.encode("ascii",errors="ignore").decode().strip("(").strip(")")
    name=brow.title[brow.title.find("to")+3:brow.title.find("-",-1)] + " by " + writer
    if len(name)>255:
        by=name[name.find("by")+2:]
        name=name[:name.find(" ",100)]+by #(len(name)-(len(name)%255+50))%255)
    for char in restricted_chars:
        #print(char)
        name=name.replace(char,' ')
    #print(name)
    pdfkit.from_url(link,os.getcwd()+"\\pdf\\%i."%serial+name+".pdf",options=options)
    #print(os.getcwd()+"\\pdf\\"+brow.title.replace("?",'')+".pdf")

def save_pdf(file_path=os.getcwd()+"\\temp.sid",start=0):
    #print(file_path)
    if not os.path.exists(file_path):
        print("No file found...")
        return
    else:
        i=0
        with open(file_path,'r') as fil:
            for j,link in enumerate(fil):
                if j>=start:
                    save_answer(link,j+1)
                    i+=1

        print("Total %i answers saved as pdf." %i)
    

def extract_links(elements,start=0):
    global brow
    global links
    global t
    for i in range(start,len(elements),2):
        try:
            ActionChains(brow).move_to_element(elements[i]).click().perform()
            time.sleep(2)
            l=brow.find_element_by_link_text('Copy Link')
            ActionChains(brow).move_to_element(l).click().perform()
            time.sleep(1)
            text=pyperclip.paste()
            print(text)
            links.append(text)
        except selenium.common.exceptions.StaleElementReferenceException:
            print("Stale Element Exception Caught for i=%i" %i)


open_credential()
#Disable Infobar on Chrome automated web browser
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
brow = webdriver.Chrome(chrome_options=chrome_options)
brow.maximize_window()

Login()
expand_page()

a=brow.find_elements_by_class_name('AnswerQuickShare')

#print("HERE")
#time.sleep(2)

extract_links(a,0)#(int(input("Enter Last Index of temp.sid file: "))-1)*2)


#url = "http://qr.ae/TUTzkR"

#save_answer(url,os.getcwd())
save_pdf(os.getcwd()+"\\temp.sid",int(input("Last Saved Answer Number: ")))

brow.close()

print("Conversion Completed")





