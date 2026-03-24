from bs4 import BeautifulSoup
from src.classes import *
import re


def parseHTML(path):
    DAY_MAP = {
        "poniedziałek": 0,
        "wtorek": 1,
        "środa": 2,
        "czwartek": 3,
        "piątek": 4,
        "sobota": 5,
        "niedziela": 6
    }

    with open(path, encoding="utf-8") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    entriesList = soup.find_all("timetable-entry")

    #course_name -> list[Group]
    courseDict = {}

    groupId = 0
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
        
        #2.3 Group key for dict
        groupKey = f"{groupType}-{groupNumber}"

        #3.1 Start time
        startEl = entry.find("span", {"slot": "time"})
        style = entry.get("style", "")
        startStr = startEl.get_text(" ", strip=True)
        mTime = re.search(r"(\d{1,2}):(\d{2})", startStr)
        if not mTime:
            continue
        h, m = map(int, mTime.groups())
        startMinutes = h * 60 + m

        #3.2 End time
        dialogEvent = entry.find("span", {"slot": "dialog-event"})
        if not dialogEvent:
            continue

        text = dialogEvent.get_text(" ", strip=True).lower()
        mEnd = re.search(r"(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})", text) #UW
        if not mEnd:
            mEnd = re.search(r"(\d{1,2}):(\d{2})\s*\u2014\s*(\d{1,2}):(\d{2})", text) #UKSW
        if mEnd:
            h1, m1, h2, m2 = map(int, mEnd.groups())
            endMinutes = h2 * 60 + m2

        #3.3 Day

        parentDay = entry.find_parent("timetable-day")
        if parentDay:
            h4 = parentDay.find_previous("h4")
            if h4:
                dayName = h4.get_text(" ", strip=True).lower()
                day = DAY_MAP.get(dayName)

        # 4. Person
        personRaw = entry.find("div", {"slot": "dialog-person"})
        if personRaw:
            person = personRaw.get_text()
            person = person.split(",")[0]

        # Creating classes
        slot = TimeSlot(day, startMinutes, endMinutes, 0)

        if courseName not in courseDict:
            courseDict[courseName] = Course(courseName)
        
        isTypeIncluded = False
        i = 0
        typeNr = 0
        for groupList in courseDict[courseName].typeList:
            if len(groupList) == 0:
                i+=1
                continue
            
            # print("type w liście:", groupList[0].type)
            # print("szukany type:", groupType)
            if groupList[0].type == groupType:
                # print("znaleziono: ", i)
                typeNr = i
                isTypeIncluded = True
                break
            i += 1
        # print(typeNr)
        if isTypeIncluded == False:
            courseDict[courseName].typeList.append([])
            typeNr = len(courseDict[courseName].typeList) - 1

        isGroupIncluded = False
        for group in courseDict[courseName].typeList[typeNr]:
            if group.giveKey() == groupKey:
                isGroupIncluded = True
                group.slotList.append(slot)

        if isGroupIncluded == False:
            groupToInsert = Group(groupType, groupNumber, person, courseDict[courseName], groupId)
            groupToInsert.slotList.append(slot)
            courseDict[courseName].typeList[typeNr].append(groupToInsert)
            groupId += 1

    #Creating plan class:
    plan = Plan()
    for course in courseDict.values():
        plan.courseList.append(course)
    return plan
    
