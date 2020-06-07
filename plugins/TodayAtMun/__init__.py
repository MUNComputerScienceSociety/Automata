# import discord
# from discord.ext import commands
from datetime import datetime

# from Plugin import AutomataPlugin

# class TodayAtMun(AutomataPlugin):


fileName = "diary.txt"

date = str(datetime.now().strftime("%Y-%#m-%#d"))
month = {
    1: "January",
    2: "Febuary",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}


dice = date.split("-")

currYear = dice[0]
currMonth = int(dice[1])
currDay = dice[2]


lookUp = f"{month[currMonth]} {currDay}, {currYear}"

print(lookUp)
fileReader = open(fileName, "r")
# fileName.close()
