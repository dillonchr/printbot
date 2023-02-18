from collections import namedtuple
import datetime

Task = namedtuple("Task", ["label", "duration"])

schedule = {
    "everyday": [
        Task("Personal Study", 20),
        Task("Walk", 30),
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


def human_readable_duration(d):
    return f"{d}m" if 60 > d else (f"{(d/60):1.1}" if 0 < d % 60 else f"{d//60}h")


def str_repeater(char, count):
    return f"{char}".join(["" for i in range(count + 1)])


def print_bar(minutes):
  chunk_size = 20 if minutes >= 60 else 5
  count = minutes // chunk_size
  max_chars = 32
  avg_size = (max_chars - 2) // count
  remainder = max_chars - avg_size * count
  lastPad = remainder // 2
  firstPad = remainder - lastPad
  out = ""

  for i in range(count):
    if 0 == i:
      segment_len = avg_size - 2 + firstPad - (1 if chunk_size < 10 else 2)
      out += "[" + str(chunk_size) + str_repeater("'", segment_len) + "|";
    elif count == i + 1:
      out += str_repeater("'", avg_size - 1 + lastPad) + "]";
    else:
      out += str_repeater("'", avg_size - 1) + "|";
  return out


if "__main__" == __name__:
    today = datetime.date.today()
    print(f"[=]{today.strftime('%b %d, %Y')}")
    tasks = schedule["everyday"] + schedule[today.strftime("%A")]
    for task in tasks:
        print(f"<=>{task.label} ({human_readable_duration(task.duration)})")
        print(f"{print_bar(task.duration)}")
        print("")

