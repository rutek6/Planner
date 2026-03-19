from bs4 import BeautifulSoup
import re

with open("plan.html", encoding="utf-8") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

entriesList = soup.find_all("timetable-entry")

#course_name -> list[Group]
courseDict = {}


for entry in entriesList:
    #1. Course name
    courseName = entry.get("name", "").strip()
    if not courseName:
        continue

    #2.1 Group type
    groupInfoRaw = entry.find("div", {"slot": "info"})
    groupInfo = groupInfoRaw.get_text(" ", strip = True)
    groupText = groupInfo.upper()
    if "CWW" in groupText:
        groupType = "CWW"
    elif "CW" in groupText:
        groupType = "CW"
    elif "WYK" in groupText:
        groupType = "WYK"
    elif "LAB" in groupText:
        groupType = "LAB"
    elif "LEK_NOW" in groupText:
        groupType = "LEK_NOW"
    elif "KON" in groupText:
        groupType = "KON"
    elif "WAR" in groupText:
        groupType = "WAR"
    elif "WF" in groupText:
        groupType = "WF"
    else:
        groupType = "UNK"
    
    #2.2 Group number with regex
    m_num = re.search(r"(\d+)", groupInfo)
    if m_num:
        groupNumber = m_num.group(1)
    else:
        groupNumber = "0"

    #3.1 Start time

    print(courseName)
    print(groupType)
    print(groupNumber)