from nextcord.ext import commands, tasks
from Plugin import AutomataPlugin

import httpx

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

## The starting page for the vaccine booking system. Used to get a valid session cookie.
START_URL = "https://portal.healthmyself.net/nleasternhealth/forms/P2E"

## The first page for the vaccine booking process. Used to get a valid session cookie.
BOOKING_URL = "https://portal.healthmyself.net/nleasternhealth/guest/booking/form/abec68ea-5a99-421b-b137-6e83cf7a3231"

## The endpoint for accessing available appointment data.
LOCATION_URL = "https://portal.healthmyself.net/nleasternhealth/guest/booking/type/5892/locations"

class Appointments(AutomataPlugin):

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)
        self._binded_channels = []
        self._previous_openings = []
    
    def cog_unload(self):
        self.vaccineupdate.cancel()
    
    ## Retrieve appointment data from the booking system endpoint.
    def get_appointment_data(self):
        with httpx.Client() as client:
            client.headers.update({'referer': START_URL})
            client.get(BOOKING_URL)
            r = client.get(LOCATION_URL)

            if (r.status_code != 200):
                return None
            else:
                return r.json()
        return None
        

    """Return the 1st shot/2nd shot/Booster COVID-19 vaccine locations with available appointments."""
    @commands.command()
    async def appointments(self, ctx: commands.Context):
        app_data = self.get_appointment_data()
        message = ""

        if (not app_data):
            message = "Request Failed!"
        else:
            ## the retreived data is a collection of (location) id, hasUnavailableAppointment pairs.

            available = []
            for row in app_data['data']:
                if (row['id'] in LOCATIONS and not row['hasUnavailableAppointments']):
                    available.append(LOCATIONS[row['id']])
            
            if (available):
                message = "Appointments available at: \n" + "\n".join(available)
            else:
                message = "No appointments available!"

        await ctx.send(message)
    
    """Add the vaccine tracker to this channel, which messages the channel upon a new appointment."""
    @commands.command()
    async def startvaccinetracker(self, ctx: commands.Context):
        self._binded_channels.append(ctx.channel)
        if (len(self._binded_channels) == 1):
            self.vaccineupdate.start()

        await ctx.send("Vaccine Tracker has been added to this channel.")
    
    """Remove the vaccine tracker from this channel."""
    @commands.command()
    async def stopvaccinetracker(self, ctx: commands.Context):
        self._binded_channels.remove(ctx.channel)
        if (len(self._binded_channels) == 0):
            self._previous_openings = []
            self.vaccineupdate.cancel()

        await ctx.send("Vaccine Tracker has been removed from this channel.")
    
    @tasks.loop(minutes=2.0)
    async def vaccineupdate(self):
        app_data = self.get_appointment_data()
        message = ""

        if (not app_data):
            message = "Request Failed!"
        else:
            ## as opposed to appointments(), the tracker loop only outputs differences in appointment status
            additions = []
            removals = []
            for row in app_data['data']:
                if (row['id'] in LOCATIONS and not row['hasUnavailableAppointments'] and not row['id'] in self._previous_openings):
                    self._previous_openings.append(row['id'])
                    additions.append(LOCATIONS[row['id']])
                elif (row['id'] in LOCATIONS and row['hasUnavailableAppointments'] and row['id'] in self._previous_openings):
                    self._previous_openings.remove(row['id'])
                    removals.append(LOCATIONS[row['id']])
            
            if (additions):
                message = "Appointments now available at: \n" + "\n".join(additions)
            if (additions and removals):
                message += "\n\n" ## put a line between additions & removals if both are present.
            if (removals):
                message += "No more appointments available at: \n" + "\n".join(removals)

        for channel in self._binded_channels:
            if (message != ""):
                await channel.send(message)
