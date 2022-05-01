from unicodedata import category
from nextcord.ext import commands

from Plugin import AutomataPlugin

import requests
import xml.etree.ElementTree as ET
import datetime
from datetime import timezone
import pytz
import random

TODAY = "TODAY"
category = ["event", "aviation", "birth", "death"] 

class DisDay(AutomataPlugin):
    """Prints a major event in history\
        
       The data retrieved is attributed to http://www.hiztory.org/
        
    """

    @commands.command()
    async def disday(self, ctx: commands.Context, today: str = " "):
        """Replies with an event in history on this day """

        
        #converting system time to newfoundland time
        utc_now = datetime.datetime.now(timezone.utc)
        newfoundland_timezone = pytz.timezone('America/St_Johns')
        current_time = utc_now.astimezone(newfoundland_timezone)
        
        ind = random.randint(0, 3)
        url  = "http://api.hiztory.org/random/{0}.xml".format(category[ind])

        #if it the argument is today, only returns an event happened today
        if today.upper() == TODAY:
            url = 'https://api.hiztory.org/date/event/{0}/{1}/api.xml'.format(current_time.month,current_time.day)
     
        r = requests.get(url)
        root = ET.fromstring(r.content)
        suffix = ""
        for child in root:
            #Event tag has the desired info
            if child.tag != 'event':
                continue
            formatted_date = datetime.datetime.strptime(child.attrib['date'], '%Y-%m-%d').strftime("%b %d %Y")
            if root.tag == 'birth':
                suffix = "was born"
            await ctx.send('On {0}, {1} {2}'.format(formatted_date,child.attrib['content'],suffix))