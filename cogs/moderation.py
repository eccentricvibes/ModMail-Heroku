import discord
from discord.ext import commands
import aiohttp
import asyncio
from discord import Forbidden
import logging
from discord.ext.commands import has_permissions
import textwrap

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_descriptions = {
            "kick": "This is a basic command that can kick somebody from the server they are sharing with the command user. You need moderator/administrator permissions to run this command.",
            "ban": "This is a basic command that can ban somebody from the server they are sharing with the command user. You need administrator permissions to run this command.",
            "get_bog_logs": "This is a command for staff members that can allow them to see the logs of what the bot has done, and what users of their server has done.",
            "help": "This command is the reason how you can see the descriptions of these commands right now!"
        }

    @commands.command()
    async def report(self, ctx, staff:discord.Member, *, message:str):
        if staff.guild_permissions.administrator:
            try:
                await staff.send(message)
                embed = discord.Embed()
                embed.add_field(name="⠀", value="Report successfully sent to the specified staff member!")
                await ctx.send(embed=embed)
            except Forbidden:
                embed = discord.Embed()
                embed.add_field(name="Oops!", value=f"{staff.name} has their dms currently turned off, so the report could not be sent.")
                await ctx.send("If you need help finding")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.add_field(name="Oops!", value="Message could not be sent, as the specified member is not a staff member, or they do not have administrator permissions.")
            await ctx.send(embed=embed)

    @commands.command()
    async def evaluate(self, ctx, *, code):
        codeblock = f"```{code}```"
        end_code = code.strip("`")
        end_code = end_code.strip("py")
        end_code = textwrap.indent(end_code, prefix="\t")
        variables = {}
        evaluated_result = exec(f"async def eval_code():\n{end_code}", variables)
        embed = discord.Embed()
        embed.add_field(name="Evaluated result: ", value=f"{await variables['eval_code']()}")
        await ctx.send(embed=embed)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason: str):
        try:
            embed = discord.Embed()
            guild = ctx.guild
            embed.add_field(name="Attempting kick for user...", value="...")
            embed2 = discord.Embed()
            embed2.add_field(name="User successfully kicked!",
                             value="Sending reason for the kick to the kicked user...")
            await guild.kick(member)
            await ctx.send(embed=embed)
            await ctx.send(embed=embed2)
            await member.send(reason)
        except Forbidden:
            embed = discord.Embed()
            embed.add_field(name="Oops!", value="You don't have the permission to kick users!")
            await ctx.send(embed)

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason: str):
        try:
            embed = discord.Embed()
            guild = ctx.guild
            embed.add_field(name="Attempting kick for user...", value="...")
            embed2 = discord.Embed()
            embed2.add_field(name="User successfully banned!",
                             value="Sending the reason for the ban to the banned user... ")
            await guild.ban(member)
            await ctx.send(embed=embed)
            await ctx.send(embed=embed2)
            await member.send(reason)
        except Forbidden:
            embed = discord.Embed()
            embed.add_field(name="Oops!", value="You don't have the permission to ban users!")
            await ctx.send(embed="")

    # @commands.command(aliases=["c_h"])
    # async def commands_help(self, ctx, bot):
    #     embed = discord.Embed()
    #     for command in bot.commands:
    #         embed.add_field(name="Command found ->", value=f"{command}")
    #     await ctx.send(embed=embed)

    @has_permissions(administrator=True)
    @commands.command()
    async def rename(self, ctx, member: discord.Member, new_name, *, reason: str):
        embed = discord.Embed()
        await member.edit(nick=new_name)
        embed.add_field(name="Renaming user...", value=f"{member.name}'s nickname was successfully changed! Sending reason to user...")
        await member.send(reason)
        await ctx.send(embed=embed)

    @commands.command()
    async def user(self, ctx, member: discord.Member):
        created_on = member.created_at.strftime("%b", "%d", "%y")
        joined_on = member.joined_on.strftime("%b", "%d", "%y")
        user_pfp = member.avatar_url()





@commands.Cog.listener()
async def on_ready():
    print("ready")
    while True:
        print("cleared")
        await asyncio.sleep(10)
        with open("user_messages.txt", "r+") as file:
            file.truncate(0)

@commands.Cog.listener()
async def on_message(self, ctx, message, bad_words):
    # counter = 0
    # guild = ctx.guild
    # for i in bad_words:
    #     if message in bad_words:
    #         await message.delete()
    #         await ctx.send(f"{message.author.mention}, that language isn't allowed here!")
    #         logging.basicConfig(filename="bot_logs.txt", filemode="r+", level="WARNING")
    #         logging.warning(message)
    #         logging.info(f"{message.author} used a bad word! Word censored was: {message.search(i)}")

    with open("spam_detection.txt", "r+") as file:
        for lines in file:
            if lines.strip('\n') == str(message.author.id):
                counter += 1
                file.writelines(f"{message.auth.id}, {message.author.name}: {message.content}")
                if counter > 5:
                    embed = discord.Embed()
                    embed.add_field(name="Uh oh!", value=f"{message.author.name, message.author.id} was muted for sending messages too quickly.")
                    spamming_user = message.author.name  




    # @commands.command()
    # async def help(self, ctx, called_command, command_descriptions):
    #     embed = discord.Embed()
    #     embed2 = discord.Embed()
    #     for command in self.bot.commands:
    #         get_command = command_descriptions.get(called_command, default="Command not found!")
    #         embed.add_field(name=f"Description for {command.name}⬇", value=f"{get_command}")
    #     await asyncio.sleep(3)
    #     embed2.add_field(name="Happy coding!", value="I hope that helped you!")
    #     await ctx.send(embed=embed)
    #     await ctx.send(embed=embed2)


def setup(bot):
    bot.add_cog(Moderation(bot))
