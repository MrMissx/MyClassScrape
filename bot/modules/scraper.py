import aiohttp

from datetime import datetime
from discord import Embed, NotFound
from pytz import timezone

from bot import bot, BOT_PREFIX, CS_GUILD_ID, LOGGER
from bot.utils import decrypt, formater, get_collection

login_url = "https://myclass.apps.binus.ac.id/Auth/Login"
url = "https://myclass.apps.binus.ac.id/Home/GetViconSchedule"
fail_text = f"**No credentials found**\nCreate it with `{BOT_PREFIX}auth.`"
WARN_TEXT = f"""**This is a default Schedule of LA04(my owner)!\nyour Schedule may vary.**
            \nYou can `{BOT_PREFIX}auth` yourself to scrape your schedule."""

SAVED_SECRET = get_collection("CREDATA")


@bot.command(aliases=['myclass', 'schedule'])
async def getclass(ctx):
    msg = await ctx.send("Give me a sec...")
    usr , sec, text = await fetch_credentials(ctx, msg)

    async with ctx.typing():    # send a typing status
        schedule = await login(ctx, usr, sec, msg)
        if not schedule:
            return
        dateold = ""

        for sched in schedule:
            if len(text) > 1602:  # break if schedule to many
                break
            date = sched["DisplayStartDate"]
            if date != dateold:
                text += f"\n:calendar_spiral: **{date}**\n\n"
                dateold = date

            time = sched["StartTime"][:-3] + "-" + \
                sched["EndTime"][:-3]  # get rid of :seconds
            classcode = sched["ClassCode"]
            classtype = sched["DeliveryMode"]
            course = sched["CourseCode"] + " - " + sched["CourseTitleEn"]
            week = sched["WeekSession"]
            session = sched["CourseSessionNumber"]

            meetingurl = None
            if classtype == "VC":
                # get zoom url if it's a VidCon
                meetingurl = sched["MeetingUrl"]

            text += formater(time, classcode, classtype,
                            course, week, session, meetingurl)

        timenow = datetime.now(timezone("Asia/Jakarta"))
        embed = Embed(color=0xff69b4, description=text, timestamp=timenow)
        embed.set_footer(text=f"By {ctx.author}")
        await ctx.send(embed=embed)
        await msg.delete()


async def fetch_credentials(context, msg=None):
    """fetch user credentials."""
    user = context.author
    text = ""
    is_cs = False

    secrt = await SAVED_SECRET.find_one({'_id': str(user.id)})
    if secrt is None:
        if (context.guild and str(context.guild.id) == CS_GUILD_ID):  # CS LA04
            LOGGER.info("CS Schedule request")
            app = await bot.application_info()
            owner = app.owner
            secrt = await SAVED_SECRET.find_one({'_id': str(owner.id)})
            is_cs = True
            text += WARN_TEXT
        else:
            await context.send(fail_text)
            if msg:
                await msg.delete()
            return None, None, None

    cht_id = secrt['secret']
    try:
        dec = decrypt(cht_id)
        if is_cs:
            data = await owner.fetch_message(dec)
        else:
            data = await user.fetch_message(dec)
        data = data.content

    except NotFound:  # message deleted
        await SAVED_SECRET.delete_one({'_id': f"{user.id}"})  # delete from db
        await context.send(fail_text)
        if msg:
            await msg.delete()
        return None, None, None

    secret = data.replace(f"{BOT_PREFIX}auth ", "")
    usr, sec = secret.split("$")
    return usr, sec, text


async def login(context, user, password, msg=None):
    """send a login request to the url
    return data
        data = data(json) request from the url.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(login_url, params={
            "Username": user,
            "Password": password,
        }) as login:
            if login.status != 200:  # wrong credentials
                await context.send("**Login Failed\nI think that your credential is wrong.**"
                                f"\nRecreate by {BOT_PREFIX}auth again")
                if msg:
                    await msg.delete()
                return None

        async with session.get(url) as data:
            result = await data.json()
    return result
