import re
import smtplib
import dryscrape
import config
from bs4 import BeautifulSoup
import time

prevGrades = []
hasBadConn = False
useragent = "Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101 Firefox/41.0"

def getGrades():
    global hasBadConn
    try:
        # go to website
        session = dryscrape.Session()
        session.set_header("User-Agent", useragent)
        session.visit(config.url)

        # log in
        user = session.at_xpath("//input[@name='studid1']")
        user.set_attr("value", config.jupiter_user)
        password = session.at_xpath("//input[@name='text_password1']")
        password.set_attr("value", config.jupiter_password)
        session.at_xpath("//div[@id='loginbtn']").click()

        # find grades
        soup = BeautifulSoup(session.body(), "lxml")
        divs = soup.findAll("div", { "class": "big" } )
        grades = []
        for i in range(2, len(divs)-2, 2):
            grade = re.search("(\d+\.\d+)", divs[i+1].getText()).group(0)
            grades.append(( divs[i].getText(), grade ))
        if hasBadConn:
            hasBadConn = False
            log("connection reestablished")
        return grades

    except Exception:
        if not hasBadConn:
            hasBadConn = True
            log("connection lost")
        return prevGrades

def compareGrades(prev, curr):
    if len(prev) == len(curr):
        for i in range(0, len(curr)):
            if prev[i][1] != curr[i][1]:
                log(curr[i][0] + " changed")
                sendText("Your " + curr[i][0] + " grade changed from " + prev[i][1] + " to " + curr[i][1] + "!")

def sendText(message):
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login(config.email, config.email_password)
    smtp.sendmail(config.email, config.phone + "@pm.sprint.com", message)

def log(msg):
    print(msg)
    f = open("jupiter.log", "a")
    f.write("[" + time.asctime() + "] " + msg + "\n")
    f.close()

log("script started")
while True:
    currGrades = getGrades()
    compareGrades(prevGrades, currGrades)
    prevGrades = currGrades

