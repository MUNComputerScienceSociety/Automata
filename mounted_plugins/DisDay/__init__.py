from nextcord.ext import commands

from Plugin import AutomataPlugin

import requests
import xml.etree.ElementTree as ET
import datetime
from datetime import timezone,timedelta
import pytz

class DisDay(AutomataPlugin):
    """Prints a major event in history\
        
       The data retrieved is attributed to http://www.hiztory.org/
        
    """

    @commands.command()
    async def disday(self, ctx: commands.Context):
        """Replies with an event in history on this day"""

        """Converting system time to newfoundland time"""
        
        utc_now = datetime.datetime.now(timezone.utc)
        newfoundland_timezone = pytz.timezone('America/St_Johns')
        current_time = utc_now.astimezone(newfoundland_timezone)
        
        url = 'https://api.hiztory.org/date/event/{0}/{1}/api.xml'.format(current_time.month,current_time.day)

        r = requests.get(url)
        root = ET.fromstring(r.content)
        for child in root:
            """Event tag has the desired info"""
            if child.tag != 'event':
                continue
            formattedDate = datetime.datetime.strptime(child.attrib['date'], '%Y-%m-%d').strftime("%b %d %Y")
            await ctx.send('On {0} in history, {1}'.format(formattedDate,child.attrib['content']))