from datetime import datetime
import logging
import uuid

from discord.ext import commands

from Plugin import AutomataPlugin
from Utils import send_code_block_maybe_as_file

logger = logging.getLogger("Agenda")


class Agenda(AutomataPlugin):
    """Handles tracking agenda items, and exporting them as markdown"""

    async def send_agenda_text(self, ctx, variant):
        items = self.agenda_items.find({})

        text = "% MUN Computer Science Society\n% Meeting Agenda\n"
        text += f"% {datetime.now().strftime('%B %e, %Y')}\n"

        while await items.fetch_next:
            item = items.next_object()

            author_postfix = ""

            if variant != "clean":
                author_postfix = f" ({item['id']})"

            text += f'\n## {item["title"]} - {item["author"]}{author_postfix}\n{item["description"]}\n'

        await send_code_block_maybe_as_file(ctx, text)

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)

    async def cog_load(self):
        self.agenda_items = self.bot.database.automata.agenda_items

    @commands.group()
    async def agenda(self, ctx):
        """Agenda management commands"""
        pass

    @agenda.command()
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx, title: str, description: str):
        """Adds an agenda item"""

        id = str(uuid.uuid4())[:8]

        item = {
            "id": id,
            "title": title,
            "description": description,
            "author": ctx.author.nick,
        }

        await self.agenda_items.insert_one(item)

        await ctx.send(f"Added item: {title} (`{id}`), with description: {description}")

    @agenda.command()
    async def view(self, ctx, variant: str = None):
        """Views all agenda items"""
        await self.send_agenda_text(ctx, variant)

    @agenda.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx):
        """Clears all agenda items"""
        await self.send_agenda_text(ctx, "clean")

        self.agenda_items.delete_many({})

        await ctx.send(f"Cleared all agenda items, output of previous items: {text}")

    @agenda.command()
    @commands.has_permissions(manage_messages=True)
    async def remove(self, ctx, id: str):
        """Removes an agenda item by id"""

        await self.agenda_items.delete_one({"id": id})

        await ctx.send(f"Removed agenda item `{id}`.")
