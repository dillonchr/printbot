from collections import namedtuple
import datetime

Task = namedtuple("Task", ["label", "duration"])

schedule = {
    "everyday": [
        Task("Personal Study", 20),
        Task("TV", 120),
        Task("Clean House", 20),
        Task("Trash Collection", 10),
        Task("Bible Reading", 15)
    ],
    "Sunday": [],
    "Monday": [Task("Prepare for Meeting", 60)],
    "Tuesday": [],
    "Wednesday": [Task("Yearbook/Interviews", 10)],
    "Thursday": [Task("Family Worship", 60)],
    "Friday": [Task("Watchtower Study", 60)],
    "Saturday": []
}

if "__main__" == __name__:
    today = datetime.date.today()
    print(f"[=]{today.strftime('%b %d %Y')}")
    tasks = schedule["everyday"] + schedule[today.strftime("%A")]
    for task in tasks:
        print(f"{task.label}")

