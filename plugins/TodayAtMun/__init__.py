import discord
from discord.ext import commands
from datetime import datetime
from month import month

#from Plugin import AutomataPlugin


class TodayAtMun():
    """
        Provides Significant Dates on the Mun Calendar
    """

    fileName = "diary.txt"
    date = str(datetime.now().strftime("%Y-%#m-%#d"))

    dice = date.split("-")

    currYear = dice[0]
    currMonth = int(dice[1])
    currDay = dice[2]

    lookUp = f"{month[currMonth]} {currDay}, {currYear}"
    
    print(lookUp)
    fileReader = open(fileName, "r")
    # fileName.close()

    @commands.Command()
    async def getCurrDate(self):
        date = str(datetime.now().strftime("%Y-%#m-%#d"))

        dice = date.split("-")

        currYear = dice[0]
        currMonth = int(dice[1])
        currDay = dice[2]

        lookUp = f"{month[currMonth]} {currDay}, {currYear}"

        send(lookUp)
    
