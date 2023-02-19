from contextlib import closing
from collections import namedtuple
import datetime
import sqlite3

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
    with closing(sqlite3.connect("tasks.db")) as connection:
        with closing(connection.cursor()) as cursor:
            today = datetime.date.today()
            print(f"[=]{today.strftime('%b %d, %Y')}")

            # we will always have something in "all" bucket so not counting results before
            # printing for this for loop
            for day, label, duration in cursor.execute("SELECT day, title, duration FROM tasks WHERE day in ('all', ?)", (today.strftime("%A"),)):
                print(f"<=>{label} ({human_readable_duration(duration)})")
                print(f"{print_bar(duration)}")
                print("")

            tomorrow = today + datetime.timedelta(days=1)
            cursor.execute(
                "SELECT title, STRFTIME('%H:%M', due) AS hour FROM tasks WHERE due BETWEEN DATE('now', 'localtime', 'start of day') AND DATE('now', 'localtime', 'start of day', '+1 day')"
            )

            due_tasks = cursor.fetchall()
            if len(due_tasks):
                print(f"[=]Due today")

                for label, due in due_tasks:
                    print(f"( )|=|{label}")
                    print(f"=>{due}")

