"""Scrape from Binus website."""

from datetime import datetime, timedelta

import aiohttp
from pytz import timezone
from discord import Embed, NotFound

from bot import bot, BOT_PREFIX, DEF_GUILD_ID, LOGGER
from bot.utils import decrypt, formater, get_collection, send_typing

LOGIN_URL = "https://myclass.apps.binus.ac.id/Auth/Login"
URL = "https://myclass.apps.binus.ac.id/Home/GetViconSchedule"
FAIL_TEXT = f"**No credentials found**\nCreate it with `{BOT_PREFIX}auth.`"
WARN_TEXT = f"""**This is a default Schedule of LA04(my owner)!\nyour Schedule may vary.**
            \nYou can `{BOT_PREFIX}auth` yourself to scrape your schedule.

"""

SAVED_SECRET = get_collection("CREDATA")


@bot.command(aliases=["myclass", "schedule"])
@send_typing
async def getclass(ctx, args: str = None, is_scheduler: bool = False):
    """Get the schedule for the user who trigger this command."""
    # pylint: disable=R0914, R0912, R0915
    user = ctx.author
    usr, sec, text = await fetch_credentials(ctx, user)

    if (usr or sec) is None:
        return

    if args:
        if args.lower() in ["now", "today"]:
            args = "0"
        elif args.lower() == "tomorrow":
            args = "1"

    schedule = await login(ctx, usr, sec)
    if not schedule:
        return

    if args is None:
        dateold = ""
        title = "**Class Schedule**"
        for sched in schedule:
            if len(text) > 1602:  # break if schedule to many
                break
            date = sched["DisplayStartDate"]
            if date != dateold:
                text += f"\n:calendar_spiral: **{date}**\n\n"
                dateold = date

            time = (
                sched["StartTime"][:-3] + "-" + sched["EndTime"][:-3]
            )  # get rid of :seconds
            classcode = sched["ClassCode"]
            classtype = sched["DeliveryMode"]
            course = sched["CourseCode"] + " - " + sched["CourseTitleEn"]
            week = sched["WeekSession"]
            session = sched["CourseSessionNumber"]
            meetingurl = None
            if classtype == "VC":
                # get zoom url if it's a VidCon
                meetingurl = sched["MeetingUrl"]

            text += formater(
                time, classcode, classtype, course, week, session, meetingurl
            )

    elif args.isnumeric():
        now = datetime.now(timezone("Asia/Jakarta")) + \
            timedelta(days=int(args))
        datewanted = now.strftime("%d %b %Y")  # dd MMM yyyy
        if args == "0":
            title = "**Schedule for Today**"
        elif args == "1":
            title = "**Schedule for Tomorrow**"
        else:
            title = f"**Schedule for {datewanted}**"

        for sched in schedule:
            dateclass = sched["DisplayStartDate"]
            if datewanted in dateclass:
                timeclass = (
                    sched["StartTime"][:-3] + "-" + sched["EndTime"][:-3]
                )  # get rid of :seconds
                classcode = sched["ClassCode"]
                classtype = sched["DeliveryMode"]
                course = sched["CourseCode"] + " - " + sched["CourseTitleEn"]
                week = sched["WeekSession"]
                session = sched["CourseSessionNumber"]
                meetingurl = None
                if classtype == "VC":
                    # get zoom url if it's a VidCon
                    meetingurl = sched["MeetingUrl"]

                text += formater(timeclass, classcode, classtype,
                                 course, week, session, meetingurl)

        if WARN_TEXT in text:
            temp = text.replace(WARN_TEXT, "")  # if use my creds
            if temp == "":
                text += "\nGreat No schedule at this date :grin:"
        elif text == "":
            text = "Great No schedule at this date :grin:"

    else:
        return await ctx.send("Unknown arguments\nRead help pls :)")

    if is_scheduler:
        user = "Auto-Scheduler"

    timenow = datetime.now(timezone("Asia/Jakarta"))
    embed = Embed(
        color=0xFF69B4,
        description=text,
        timestamp=timenow,
        title=title)
    embed.set_footer(text=f"By {user}")
    await ctx.send(embed=embed)


async def fetch_credentials(context, user):
    """fetch user credentials."""
    text = ""
    is_cs = False

    secrt = await SAVED_SECRET.find_one({"_id": str(user.id)})
    if secrt is None:
        if context.guild and context.guild.id == DEF_GUILD_ID:
            LOGGER.info("Default guild schedule request")
            app = await bot.application_info()
            owner = app.owner
            secrt = await SAVED_SECRET.find_one({"_id": str(owner.id)})
            is_cs = True
            text += WARN_TEXT
        else:
            await context.send(FAIL_TEXT)
            return None, None, None

    cht_id = secrt["secret"]
    try:
        dec = decrypt(cht_id)
        if is_cs:
            data = await owner.fetch_message(dec)
        else:
            data = await user.fetch_message(dec)
        data = data.content

    except NotFound:  # message deleted
        await SAVED_SECRET.delete_one({"_id": f"{user.id}"})  # delete from db
        await context.send(FAIL_TEXT)
        return None, None, None

    secret = data.replace(f"{BOT_PREFIX}auth ", "")
    usr, sec = secret.split("$")
    return usr, sec, text


async def login(context, user, password):
    """send a login request to the url
    return data
        data = data(json) request from the url.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
                LOGIN_URL,
                json={
                    "Username": user,
                    "Password": password,
                },
        ) as auth:
            if auth.status != 200:
                await context.send(
                    "**Login Failed!\nThis most likely caused by server issue.**"
                )
                return None
            res = await auth.json()
            if not res["Status"]:
                await context.send(
                    f"**Login Failed.\n**"
                    f"Server response: \"{res['Message']}\""
                )
                return None

        async with session.get(URL) as data:
            result = await data.json()
    return result
