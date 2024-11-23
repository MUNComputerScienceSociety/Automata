import logging
import uuid
from datetime import datetime

from discord.ext import commands

from automata.mongo import mongo
from automata.utils import CommandContext, Plugin, send_code_block_maybe_as_file

logger = logging.getLogger("Agenda")


class Agenda(Plugin):
    """Handles tracking agenda items, and exporting them as markdown"""

    async def send_agenda_text(self, ctx: CommandContext, variant: str | None):
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

    async def cog_load(self):
        self.agenda_items = mongo.automata.agenda_items

    @commands.group()
    async def agenda(self, ctx: CommandContext):
        """Agenda management commands"""
        pass

    @agenda.command()
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx: CommandContext, title: str, description: str):
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
    async def view(self, ctx: CommandContext, variant: str | None = None):
        """Views all agenda items"""
        await self.send_agenda_text(ctx, variant)

    @agenda.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: CommandContext):
        """Clears all agenda items"""
        await self.send_agenda_text(ctx, "clean")

        self.agenda_items.delete_many({})

        await ctx.send("Cleared all agenda items")

    @agenda.command()
    @commands.has_permissions(manage_messages=True)
    async def remove(self, ctx: CommandContext, id: str):
        """Removes an agenda item by id"""

        await self.agenda_items.delete_one({"id": id})

        await ctx.send(f"Removed agenda item `{id}`.")
