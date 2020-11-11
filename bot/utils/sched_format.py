def formater(time, classcode, classtype, course, week, session, meetingurl):
    output = (
        f"**Time :** {time}\n"
        f"**Class :** {classcode} - {classtype}\n"
        f"**course :** {course}\n"
        f"**week/session :** {week}/{session}\n"
    )
    if meetingurl != "-":
        output += f"[Meeting URL]({meetingurl})\n\n"
    else:
        output += "\n"
    return output