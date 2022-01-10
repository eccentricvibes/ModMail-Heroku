import discord
from discord.ext import commands
import aiohttp
import asyncio
from discord import Forbidden
import logging
from discord.ext.commands import has_permissions
import textwrap
from bs4 import BeautifulSoup
import requests
import mysql.connector
from googlesearch import search
import os
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.command_descriptions = {
            "kick": "This is a basic command that can kick somebody from the server they are sharing with the command user. You need moderator/administrator permissions to run this command.",
            "ban": "This is a basic command that can ban somebody from the server they are sharing with the command user. You need administrator permissions to run this command.",
            "get_bog_logs": "This is a command for staff members that can allow them to see the logs of what the bot has done, and what users of their server has done.",
            "help": "This command is the reason how you can see the descriptions of these commands right now!"
        }
        self.user_events = {}
        # mydb = mysql.connector.connect(
        #     host="localhost",
        #     user=os.environ["DB_USER"],
        #     password=os.environ["DB_PASSWORD"],
        # )
        # mycursor = mydb.cursor()


        # mycursor.execute()
    @commands.command()
    async def report(self, ctx, user: discord.Member, staff: discord.Member, *, message: str):
        if staff.guild_permissions.administrator:
            try:
                report_embed = discord.Embed()
                report_embed.add_field(name=f"Report sent from {str(ctx.author)}!", value=f"Report sent regarding {user}, reason: {message}")
                await staff.send(embed=report_embed)
                embed = discord.Embed()
                embed.add_field(name="⠀", value="Report successfully sent to the specified staff member, they will respond whenever they have the time to.")
                await ctx.send(embed=embed)
            except Forbidden:
                embed = discord.Embed()
                embed.add_field(name="Oops!",
                                value=f"{staff.name} has their dms currently turned off, so the report could not be sent.")
                await ctx.send("If you need help finding")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.add_field(name="Oops!",
                            value="Message could not be sent as the specified member is not a staff member, or they do not have administrator permissions.")
            await ctx.send(embed=embed)

    @commands.command()
    async def reply(self, ctx, member: discord.Member, *, response: str):
        embed = discord.Embed()
        embed.add_field(name=f"Reply to {member.name, member.id}'s report", value=f"{ctx.author.name}: {response}")
        embed2 = discord.Embed()
        embed.add_field(name="")
        await member.send(embed=embed)

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

    @has_permissions(administrator=True)
    @commands.command()
    async def clear(self, ctx, amount: int):
        embed = discord.Embed(description=f"Successfully cleared {amount} messages!")
        await ctx.channel.purge(1)
        await ctx.channel.purge(amount)
        await ctx.send(embed=embed)


    # @commands.command()
    # async def commands_help(self, ctx):
    #     for page in self.paginator.pages:
    #         embed = discord.Embed(description=page)
    #         await ctx.send(embed=embed)





    @commands.command()
    async def mute(self, user: discord.Member, *, reason: str):
        embed = discord.Embed()

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
        embed.add_field(name="Renaming user...",
                        value=f"{member.name}'s nickname was successfully changed! Sending reason to user...")
        await member.send(reason)
        await ctx.send(embed=embed)

    @commands.command()
    async def user(self, ctx, member: discord.Member):
        created_on = member.created_at.strftime("%A, %B %d %Y: %H:%M:%S %p")
        joined_on = member.joined_at.strftime("%A, %B %d %Y: %H:%M:%S %p")
        user_pfp = member.avatar_url
        embed = discord.Embed()
        embed.add_field(name=f"User information", value=f"User created on {created_on}\nUser joined on {joined_on}\nLink to user's profile picture {user_pfp}")
        await ctx.send(embed=embed)

    @commands.command()
    async def rtfm(self, ctx, *, keywords: str):
        embed = discord.Embed()
        for query in search(keywords, tld="co.in", num=5, start=0, stop=5, pause=3):
            embed.add_field(name="Result found!", value=f"{query}")
        await ctx.send(embed=embed)
        await asyncio.sleep(20)
        await ctx.delete_message()

    @commands.command()
    async def create_event_reminder(self, ctx, time, *, event: str, members: discord.Member):
        start_time = datetime.datetime.now()
        end_time = start_time + time
        end_time1 = end_time.strftime("%a, %b %d, %Y")
        end_time2 = end_time.strftime("%I: %M:%S %p")
        embed = discord.Embed()
        await embed.add_field(name=f"Event set: {event}", value=f"Time set for reminder: {end_time1} at {end_time2}. No need to worry, ModMail will remind all the specified users, at the specified time for the event.")
        members = list(members)
        member_list = []
        for member in members:
            member_list.append(member)
            self.user_events[member] = f"{event}, {end_time1} at {end_time2}"
        if datetime.datetime.now() == end_time1 and end_time2:
            for member in self.user_events.keys():
                embed = discord.Embed()
                await embed.add_field(name=f"There's an event coming up, {event}", value=f"{await ctx.mention(member)}, this event was scheduled for you!")
            var = await ctx.send(embed=embed)
            reaction_check = await var.add_reaction("✅")
            reaction_x = await var.add_reaction("❌")

            
    commands.has_permissions(administrator=True)
    @commands.command()
    async def serverinfo(self, ctx):
        request_time = datetime.datetime.now()
        embed = discord.Embed(title="Info for {}".format(ctx.message.server.name), description="Information about the server")
        await embed.add_field(name="Server name: ", value=ctx.message.server.name, inline=True)
        await embed.add_field(name="Server id: ", value=ctx.message.server.id, inline=True)
        await embed.add_field(name="Server members: ", value=f"{len(ctx.message.server.members)}", inline=True)
        await embed.add_field(name="Server owner: ", value=ctx.message.server.owner, inline=True)
        await embed.add_field(name="Server roles: ", value=f"{len(ctx.message.server.roles)}", inline=True)

        servermade = ctx.message.server.

        await embed.set_footer(text=f"{ctx.message.author} requested server information at {request_time.strftime('%H:%M:%S')} on {request_time.strftime('%m/%d/%Y')}")


    @commands.command()
    async def mute(self, ctx, member: discord.Member, *, reason: str):



    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        embed = discord.Embed()

    # @commands.command()
    # async def store(self, ctx):


        # search_message = soup.select(".search-summary")
        # search_embed = soup.select("grid-item #search-results .search")
        # query_li_tag = soup.select_all("li", class_="style")
        # query_result_link = query_li_tag.get("href")
        # result_description = soup.select(".grid-item #search-results .search .context").text
        # embed = discord.Embed()
        # embed.add_field(name="Querying on discord.py's documentation...", value=f"{search_message}\n{query_result_link}\n{result_description}")
        # await ctx.send(embed=embed)

    # @commands.command()
    # async def rtfm(self, ctx, *, keywords: str):
    #     response = requests.get(f"https://www.google.com/search?q={keywords}")
    #     html = response.text
    #     soup = BeautifulSoup(html, "lxml")
    #     page_list = soup.select("")
    #
    # @command.command()
    # async def warn(self, cftx: Context, ):



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
    counter = 0
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
                    embed.add_field(name="Uh oh!",
                                    value=f"{message.author.name, message.author.id} was muted for sending messages too quickly.")
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
