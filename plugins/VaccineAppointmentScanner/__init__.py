from nextcord.ext import commands, tasks
from Plugin import AutomataPlugin

import requests

## Mapping of major St. John's vaccine location IDs to location names
LOCATIONS = {
    949: "The Village Mall YELLOW",
    943: "The Village Mall BLUE",
    776: "FORMER Public Service Commission Building (50 Mundy Pond Road) (Ages <29)",
    1668: "The Village Mall RED",
    1669: "The Village Mall GREEN",
    814: "Reid Community Centre (Location A) (Ages 30+)",
    1672: "Reid Community Centre (Location B) (Ages 30+)",
    1673: "Reid Community Centre (Location C) (Ages 30+)"
}

## The endpoint for accessing available appointment data.
URL = "https://portal.healthmyself.net/nleasternhealth/guest/booking/type/5892/locations"

class Appointments(AutomataPlugin):

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)
        self._code = ""
        self._binded_channels = []
        self._previous_openings = []
        self.vaccineupdate.start()
    
    def cog_unload(self):
        self.vaccineupdate.cancel()

    """Return the 1st shot/2nd shot/Booster COVID-19 vaccine locations with available appointments."""
    @commands.command()
    async def appointments(self, ctx: commands.Context):
        ## Accessing appointment data requires a valid hm_session cookie. We must artificially create
        ## this cookie to gain access to this information.
        ## (there is probably a much easier way to do this)
        session = requests.Session()
        session.cookies.set('hm_session', self._code)

        r = session.get(URL)
        if (r.status_code != 200):
            message = "Request Failed! Set the hm_session code first with !setvaccinecode"
        else:
            available = []
            raw_json = r.json()
            
            ## the retreived data is a collection of (location) id, hasUnavailableAppointment pairs.
            for row in raw_json['data']:
                if (row['id'] in LOCATIONS and not row['hasUnavailableAppointments']):
                    available.append(LOCATIONS[row['id']])
            
            if (available):
                message = "Appointments available at: \n" + "\n".join(available)
            else:
                message = "No appointments available!"

        await ctx.send(message)
    
    """Set the hm_session cookie code for accessing vaccine information."""
    @commands.command()
    async def setvaccinecode(self, ctx: commands.Context, message: str):
        self._code = message

        await ctx.send("hm_session vaccine code has been set!")
    
    """Add the vaccine tracker to this channel, which messages the channel upon a new appointment."""
    @commands.command()
    async def startvaccinetracker(self, ctx: commands.Context):
        self._binded_channels.append(ctx.channel)
        await ctx.send("Vaccine Tracker has been added to this channel.")
    
    """Remove the vaccine tracker from this channel."""
    @commands.command()
    async def stopvaccinetracker(self, ctx: commands.Context):
        self._binded_channels.remove(ctx.channel)
        await ctx.send("Vaccine Tracker has been removed from this channel.")
    
    @tasks.loop(minutes=2.0)
    async def vaccineupdate(self):
        if (not self._binded_channels):
            self._previous_openings = []
            return

        session = requests.Session()
        session.cookies.set('hm_session', self._code)
        message = ""

        r = session.get(URL)
        if (r.status_code != 200):
            message = "Request Failed! Set the hm_session code first with !setvaccinecode"
        else:
            additions = []
            removals = []
            raw_json = r.json()

            ## as opposed to appointments(), the tracker loop only prints differences in appointment status
            for row in raw_json['data']:
                if (row['id'] in LOCATIONS and not row['hasUnavailableAppointments'] and not row['id'] in self._previous_openings):
                    self._previous_openings.append(row['id'])
                    additions.append(LOCATIONS[row['id']])
                elif (row['id'] in LOCATIONS and row['hasUnavailableAppointments'] and row['id'] in self._previous_openings):
                    self._previous_openings.remove(row['id'])
                    removals.append(LOCATIONS[row['id']])
            
            if (additions):
                message = "Appointments now available at: \n" + "\n".join(additions)
            if (additions and removals):
                message += "\n"
            if (removals):
                message += "No more appointments available at: \n" + "\n".join(removals)

        for channel in self._binded_channels:
            if (message != ""):
                await channel.send(message)
