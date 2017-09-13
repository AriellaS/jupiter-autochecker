import re
from bs4 import BeautifulSoup
import dryscrape
import time
import config

prevGrades = []

def getGrades():
    try:
        session = dryscrape.Session()
        session.visit(config.ssoURL)
        res = session.body()
        soup = BeautifulSoup(res, "lxml")
        divs = soup.findAll("div", { "class": "big" } )

        grades = []

        for i in range(2, len(divs)-2, 2):
            grade = re.search("(\d+\.\d+)", divs[i+1].getText()).group(0)
            grades.append(( divs[i].getText(), grade ))

        return grades
    except:
        return prevGrades

def compareGrades(prev, curr):
    if len(prev) == len(curr):
        for i in range(0, len(curr)):
            if prev[i][1] != curr[i][1]:
                print "Your " + curr[i][0] + " grade changed!"

while True:
    currGrades = getGrades()
    compareGrades(prevGrades, currGrades)
    prevGrades = currGrades
    time.sleep(config.waitTime)
