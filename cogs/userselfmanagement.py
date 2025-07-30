# Discord bot: cogs/userselfmanagement.py

import logging
import discord
from discord import app_commands
from discord.ext import commands

log = logging.getLogger("discord")

# List of roles users are allowed to self-assign
ALLOWED_ROLES = ["python", "javascript", "php", "c#"]


class UserSelfManagement(commands.Cog):
    """Allow users to manage themselves."""

    def __init__(self, bot):
        self.bot = bot

    # Allow users to change their own nickname
    @app_commands.command(name="nick", description="Change your nickname in this server")
    @app_commands.describe(new_nick="Your new nickname")
    async def nick(self, interaction: discord.Interaction, new_nick: str):
        try:
            await interaction.user.edit(nick=new_nick)
            await interaction.response.send_message(f"Nickname changed to: {new_nick}", ephemeral=True)
            log.info(f"{interaction.user} changed their nickname to {new_nick} in {interaction.guild.name}")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to change your nickname.", ephemeral=True)
            log.warning(f"{interaction.user} tried to change nickname but lacked permissions in {interaction.guild.name}")
        except Exception as e:
            await interaction.response.send_message("Something went wrong.", ephemeral=True)
            log.error(f"Error changing nickname for {interaction.user} in {interaction.guild.name}: {e}")

    # Allow users to add/remove whitelisted roles
    @app_commands.command(name="role", description="Add or remove an allowed role")
    @app_commands.describe(action="Choose add or remove", role="The role to self-assign")
    @app_commands.choices(
        action=[
            app_commands.Choice(name="Add", value="add"),
            app_commands.Choice(name="Remove", value="remove"),
        ],
        role=[
            app_commands.Choice(name=role, value=role) for role in ALLOWED_ROLES
        ],
    )
    async def role(self, interaction: discord.Interaction, action: app_commands.Choice[str], role: app_commands.Choice[str]):
        guild_role = discord.utils.get(interaction.guild.roles, name=role.value)

        if guild_role is None:
            await interaction.response.send_message(f"Role `{role.value}` not found on this server.", ephemeral=True)
            return

        try:
            if action.value == "add":
                if guild_role in interaction.user.roles:
                    await interaction.response.send_message(f"You already have the `{role.value}` role.", ephemeral=True)
                else:
                    await interaction.user.add_roles(guild_role)
                    await interaction.response.send_message(f"Added the `{role.value}` role.", ephemeral=True)
                    log.info(f"{interaction.user} added themselves to role {role.value} in {interaction.guild.name}")

            elif action.value == "remove":
                if guild_role not in interaction.user.roles:
                    await interaction.response.send_message(f"You don’t have the `{role.value}` role.", ephemeral=True)
                else:
                    await interaction.user.remove_roles(guild_role)
                    await interaction.response.send_message(f"Removed the `{role.value}` role.", ephemeral=True)
                    log.info(f"{interaction.user} removed the {role.value} role in {interaction.guild.name}")

        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to manage that role.", ephemeral=True)
            log.warning(f"Lacking permissions to modify role {role.value} for {interaction.user} in {interaction.guild.name}")
        except Exception as e:
            await interaction.response.send_message("Something went wrong.", ephemeral=True)
            log.error(f"Error updating role {role.value} for {interaction.user} in {interaction.guild.name}: {e}")


async def setup(bot) -> None:
    await bot.add_cog(UserSelfManagement(bot))
