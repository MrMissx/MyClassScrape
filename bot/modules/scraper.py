"""Scrape from Binus website."""

from datetime import datetime, timedelta
from typing import Dict, Optional

import aiohttp
from bs4 import BeautifulSoup
from discord import Embed, NotFound
from pytz import timezone

from bot import BOT_PREFIX, DEF_GUILD_ID, LOGGER, bot
from bot.utils import (decrypt, exam_formater, get_collection,
                       schedule_formater, send_typing)

FAIL_TEXT = f"**No credentials found**\nCreate it with `{BOT_PREFIX}auth.`"
WARN_TEXT = f"""**This is a default Schedule of my owner!\nyour Schedule may vary.**
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

    schedule = await fetch_schedule(ctx, usr, sec)
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

            text += schedule_formater(
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

                text += schedule_formater(timeclass, classcode, classtype,
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


@bot.command(aliases=["getexam", "myexam"])
@send_typing
async def exam(ctx):
    user = ctx.author
    usr, sec, _ = await fetch_credentials(ctx, user)
    if (usr or sec) is None:
        return

    data = await fetch_exam(ctx, usr, sec)
    if not data:
        return await ctx.send("Failed to fetch exam schedule!")
    exam_data = data["examSchedule"]
    if exam_data["EligibleStatus"] != 1:
        await ctx.send(
            "**Failed to fetch exam schedule!**\n"
            f"**Response:** {exam_data['EligibleDescs']}")
        return
    exam_data = exam_data["ListExam"]
    title = exam_data[0]["Component"] + " Schedule"  # Exam type
    etype = exam_data[0]["ExamType"]
    text = ""
    for exam in exam_data:
        if exam["ExamType"] == etype:
            classcode = exam["Class"]
            course = exam["CourseCode"] + " - " + exam["CourseTitle"]
            start = exam["ExamStartTime"] + ", " + exam["StartDateToDisplay"]
            end = exam["ExamShift"] + ", " + exam["EndDateToDisplay"]
            text += exam_formater(classcode, course, start, end)

    text += "Go to [Exam website](https://exam.apps.binus.ac.id/)"
    embed = Embed(
        color=0x0B6623,
        description=text,
        title=title,
        url="https://exam.apps.binus.ac.id/")
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
    raw_text = secret.split("$")
    if len(raw_text) > 2:  # handle if password contain seperator character
        usr = raw_text[0]
        sec = "$".join(raw_text[1:])
    else:
        usr, sec = raw_text
    return usr, sec, text


async def fetch_schedule(context, user, password) -> Optional[Dict]:
    """Fetch a class schedule"""
    async with aiohttp.ClientSession() as session:
        async with session.post(
                "https://myclass.apps.binus.ac.id/Auth/Login",
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

        async with session.get(
            "https://myclass.apps.binus.ac.id/Home/GetViconSchedule"
        ) as data:
            result = await data.json()
    return result


async def fetch_exam(context, user, password) -> Optional[Dict]:
    """Fetch an exam schedule"""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://exam.apps.binus.ac.id/Auth/Login",
            json={
                "username": user,
                "password": password
            }
        ) as auth:
            if auth.status != 200:
                await context.send(
                    "**Login Failed!\n"
                    "This most likely caused by server issue.**"
                )
                return None
            res = await auth.json()
            if not res["Status"]:
                await context.send(
                    f"**Login Failed.\n**"
                    f"Server response: \"{res['Message']}\""
                )
                return None

        async with session.get(
            "https://exam.apps.binus.ac.id/Home/Exam"
        ) as web:
            raw_html = await web.read()
            soup = BeautifulSoup(raw_html, "html.parser")
            tag = soup.find(id="ddlPeriod").find_all("option")
            exam_key = tag[len(tag) - 1]["value"]  # Get the latest exam key

        async with session.post(
            "https://exam.apps.binus.ac.id/Home/GetExamSchedule",
            json={"key": exam_key}
        ) as data:
            return await data.json()
