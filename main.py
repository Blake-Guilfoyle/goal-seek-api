import numpy as np
import json
from datetime import datetime
from WhatIfAnalysis import GoalSeek
#   WhatIFAnalysis Developed by Hakan İbrahim Tol, PhD
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel, create_model
from typing import List, Optional, Dict


app = FastAPI()

class scheduleItem(BaseModel):
    date: str
    interest: int
    drawdowns: int
    repayments: int
    estimated: str

class scheduleData(BaseModel):
    data: List[scheduleItem]




@app.get("/")
def read_root():
    return {"Hello":"world"}

@app.post("/goal")
def runGoalSeek(schedule:scheduleData):
    global scheduleDataList
    scheduleDataList = schedule.data

  
    def scheduleFunc(x):
        index = -1
        for item in scheduleDataList:
            index = index + 1
            
            if index == 0:
                startAmount = 0
                endAmount = item.interest + item.drawdowns - item.repayments
                # print({"date":item.date,"startAmount":0,"interest":item.interest ,"drawdowns":item.drawdowns,"repayments":item.repayments,"endAmount":endAmount})
            else:
                startAmount = endAmount
                priorItem = scheduleDataList[index - 1]
                currentDate =  datetime.strptime(item.date,"%d-%b-%Y")
                priorDate = datetime.strptime(priorItem.date, "%d-%b-%Y") 
                daysDiff = (abs((currentDate - priorDate).days))
                interestPayable = startAmount * x * ((daysDiff)/365)
                endAmount = startAmount + interestPayable + item.drawdowns - item.repayments
                # print({"Date":item.date,"startAmount":startAmount,"interest":interestPayable,"drawdowns":item.drawdowns,"repayments":item.repayments,"endAmount":endAmount})     

        return endAmount
    goal=0
    x0=0.001
    
    result=GoalSeek(scheduleFunc,goal,x0)

    updatedScheduleItems = []
    updatedLoanSchedule = {}
    updatedLoanSchedule["eir"] = result
    index = -1
    for item in scheduleDataList:
        index = index + 1
        
        if index == 0:
            startAmount = 0
            endAmount = item.interest + item.drawdowns - item.repayments
            updatedScheduleItems.append({"date":item.date,"startAmount":0,"interest":item.interest ,"drawdowns":item.drawdowns,"repayments":item.repayments,"endAmount":endAmount})
        else:
            startAmount = endAmount
            priorItem = scheduleDataList[index - 1]
            currentDate =  datetime.strptime(item.date,"%d-%b-%Y")
            priorDate = datetime.strptime(priorItem.date, "%d-%b-%Y") 
            daysDiff = (abs((currentDate - priorDate).days))
            interestPayable = startAmount * result * ((daysDiff)/365)
            endAmount = startAmount + interestPayable + item.drawdowns - item.repayments
            updatedScheduleItems.append({"date":item.date,"startAmount":round(startAmount,2),"interest":round(interestPayable,2),"drawdowns":item.drawdowns,"repayments":item.repayments,"endAmount":round(endAmount,2)})     


    updatedLoanSchedule["scheduleItems"] = updatedScheduleItems
    return updatedLoanSchedule


#with open('data.json') as f:
#    data = json.load(f)

#def scheduleFunc(x):
#    schedule = data
#    index = -1
#    for item in schedule:
#        index = index + 1
#        
#        if index == 0:
#            startAmount = 0
#            endAmount = item["interest"] + item["drawdowns"] - item["repayments"]
#            print({"Date":item["date"],"startAmount":0,"interest":item["interest"] ,"drawdowns":item["drawdowns"],"repayments":item["repayments"],"endAmount":endAmount})
#        else:
#            startAmount = endAmount
#            priorItem = schedule[index - 1]
#            currentDate =  datetime.strptime(item["date"],"%d-%b-%Y")
#            priorDate = datetime.strptime(priorItem["date"], "%d-%b-%Y") 
#            daysDiff = (abs((currentDate - priorDate).days))
#            interestPayable = startAmount * x * ((daysDiff)/365)
#            endAmount = startAmount + interestPayable + item["drawdowns"] - item["repayments"]
#            print({"Date":item["date"],"startAmount":startAmount,"interest":interestPayable,"drawdowns":item["drawdowns"],"repayments":item["repayments"],"endAmount":endAmount})     

#    return endAmount

# (ii)  Define the goal (result)
#goal=0
# (iii) Define a starting point
#x0=0.001
## Here is the result
#result=GoalSeek(scheduleFunc,goal,x0)
#print('Result of Example 1 is = ', result)

