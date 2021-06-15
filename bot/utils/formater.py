# pylint: disable=R0913
"""Format a schedule for easy reading."""

def schedule_formater(
        time,
        classcode,
        classtype,
        course,
        week,
        session,
        meetingurl=None) -> str:
    """Format schedule text"""
    output = (
        f"**Time :** {time}\n"
        f"**Class :** {classcode} - {classtype}\n"
        f"**course :** {course}\n"
        f"**week/session :** {week}/{session}\n"
    )
    if meetingurl:
        output += f"[Meeting URL]({meetingurl})\n\n"
    else:
        output += "\n"
    return output


def exam_formater(classcode, course, start_date, end_date) -> str:
    output = (
        f":school: **Class :** {classcode}\n"
        f":pushpin: **Course :** {course}\n"
        f":calendar_spiral: **Start Date :** {start_date}\n"
        f":calendar_spiral: **Deadline :** {end_date}\n\n"
    )
    return output
