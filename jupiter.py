import re
import dryscrape
import config
from bs4 import BeautifulSoup

prevGrades = []
useragent = "Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101 Firefox/41.0"

def getGrades():

    # go to website
    session = dryscrape.Session()
    session.set_header("User-Agent", useragent)
    session.visit(config.url)

    # log in
    user = session.at_xpath("//input[@name='studid1']")
    user.set_attr("value", config.user)
    password = session.at_xpath("//input[@name='text_password1']")
    password.set_attr("value", config.password)
    session.at_xpath("//div[@id='loginbtn']").click()

    # find grades
    soup = BeautifulSoup(session.body(), "lxml")
    divs = soup.findAll("div", { "class": "big" } )
    grades = []
    for i in range(2, len(divs)-2, 2):
        grade = re.search("(\d+\.\d+)", divs[i+1].getText()).group(0)
        grades.append(( divs[i].getText(), grade ))

    return grades

def compareGrades(prev, curr):
    if len(prev) == len(curr):
        for i in range(0, len(curr)):
            if prev[i][1] != curr[i][1]:
                print "Your " + curr[i][0] + " grade changed!"

while True:
    currGrades = getGrades()
    compareGrades(prevGrades, currGrades)
    prevGrades = currGrades

