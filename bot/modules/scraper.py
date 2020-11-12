import requests
import discord

from bot import bot, BOT_PREFIX
from bot.utils import formater, decrypt
import bot.modules.sql.cred_sql as saved
from datetime import datetime
from pytz import timezone

login_url="https://myclass.apps.binus.ac.id/Auth/Login"
url = "https://myclass.apps.binus.ac.id/Home/GetViconSchedule"


@bot.command(aliases=['myclass', 'schedule'])
async def getclass(ctx):
    msg = await ctx.send("Give me a sec...")
    user = ctx.author.id
    usr, sec = getcred(user)

    session = requests.Session()
    with session.post(login_url, data={
        "Username" : usr,
        "Password" : sec,
    }) as login:
        if login.cookies.get('ASP.NET_SessionId') is None:  # wrong credentials
            await ctx.send(f"**Login Failed\nI think that your credential is wrong.** \
                            \nRecreate by {BOT_PREFIX}auth again")
            await msg.delete()
            return

    with session.post(url) as data:
        schedule = data.json()
        text = ""
        count=0
        dateold = ""

        for sched in schedule:
            if count > 5:  # only scrape 5 days cause discord max msg limitation
                break
            date = sched["DisplayStartDate"]
            if date != dateold:
                count+=1
                text += f"\n# **{date}**\n\n"
                dateold=date

            time = sched["StartTime"][:-3] + "-" + sched["EndTime"][:-3]  # get rid of :seconds
            classcode = sched["ClassCode"]
            classtype = sched["DeliveryMode"]
            course = sched["CourseCode"] + " - " + sched["CourseTitleEn"]
            week = sched["WeekSession"]
            session = sched["CourseSessionNumber"]

            if classtype == "VC":
                meetingurl = sched["MeetingUrl"]  #  get zoom url if it's a VidCon
            else:
                meetingurl = "-"

            text += formater(time, classcode, classtype, course, week, session, meetingurl)
        timenow = datetime.now(timezone("Asia/Jakarta"))
        author = ctx.author.name + "#" + ctx.author.discriminator  
        embed = discord.Embed(color=0xff69b4, description=text, timestamp=timenow)
        embed.set_footer(text=f"By {author}")
        await ctx.send(embed=embed)
        await msg.delete()


def getcred(user):
    a, b = saved.get_cred(user)
    if a is None or b is None:
        return
    return decrypt(a), decrypt(b)

