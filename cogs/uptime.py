#!/usr/bin/env python3
# Discord bot: cogs/uptime.py

import logging
import socket

import discord
from config import admin_guild
from discord import app_commands
from discord.ext import commands
from process_uptime import getuptime
import datetime

log = logging.getLogger("discord")


class UptimeCog(commands.Cog):
    """Uptime command."""

    def __init__(self, bot):
        self.bot = bot
        self.sessions: set[int] = set()
        self.hostname = socket.gethostname()

    @app_commands.command()
    @app_commands.guilds(discord.Object(id=admin_guild))
    async def uptime(self, ctx: commands.Context) -> None:
        """Prints the bot uptime."""
        try:
            uptime = getuptime()
            uptimeDays = int(uptime // 60 // 60 // 24)
            uptimeHours = (uptime // 60 // 60) % 24
            uptimeMinutes = (uptime // 60) % 60
            uptimeSeconds = uptime % 60
            await ctx.response.send_message("Uptime: " + str(uptimeDays) + "d " + str(uptimeHours) + "h " + str(uptimeMinutes) + "m " + str(uptimeSeconds) + "s . \N{OK HAND SIGN}", ephemeral=True)
            log.info(f"Uptime: Command {ctx.command.name} was executed successfully in {ctx.guild.name}.")
        except commands.ExtensionError as e:
            await ctx.response.send_message(f"{e.__class__.__name__}: {e}", ephemeral=True)
            log.error(f"Uptime: Command {ctx.command.name} failed in {ctx.guild.name}.")

    @app_commands.command()
    @app_commands.guilds(discord.Object(id=admin_guild))
    async def whattimeisit(self, ctx: commands.Context) -> None:
        """Prints what time the bot thinks it is now."""
        try:
            timenow = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
            await ctx.response.send_message("I think the time is: " + str(timenow) + " . \N{OK HAND SIGN}", ephemeral=True)
            log.info(f"Uptime: Command {ctx.command.name} was executed successfully in {ctx.guild.name}.")
        except commands.ExtensionError as e:
            await ctx.response.send_message(f"{e.__class__.__name__}: {e}", ephemeral=True)
            log.error(f"Uptime: Command {ctx.command.name} failed in {ctx.guild.name}.")

async def setup(bot):
    await bot.add_cog(UptimeCog(bot))
