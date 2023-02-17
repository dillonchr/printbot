const moment = require("moment");
const lineChar = "'";
const schedule = {
  everyday: [
    { label: "Personal Study", duration: 20 },
    { label: "Walk", duration: 30 },
    { label: "TV", duration: 120 },
    { label: "Clean House", duration: 20 },
    { label: "Trash Collection", duration: 10 },
    { label: "Bible Reading", duration: 15 }
  ],
  monday: [{ label: "Prepare for Meeting", duration: 60 }],
  wednesday: [{ label: "Yearbook/Interviews", duration: 10 }],
  thursday: [{ label: "Family Worship", duration: 60 }],
  saturday: [{ label: "Watchtower Study", duration: 60 }]
};

function prepareChecklist() {
  const tasks = schedule.everyday.slice(0);
  const todayKey = moment().format("dddd").toLowerCase();
  if (todayKey in schedule) {
    tasks.push(...schedule[todayKey]);
  }
  return tasks;
}

function getHumanReadableDuration(duration) {
  return duration < 60
    ? `${duration}m`
    : 0 < duration % 60
    ? `${(duration / 60).toFixed(1)}h`
    : `${duration / 60}h`;
}

function printBar(minutes) {
  const chunkSize = minutes >= 60 ? 20 : 5;
  const count = minutes / chunkSize;
  const max = 32;
  const avgSize = Math.floor((max - 2) / count);
  const remainder = max - avgSize * count;
  const lastPad = Math.floor(remainder / 2);
  const firstPad = remainder - lastPad;

  let out = "";
  for (let i = 0; i < count; i++) {
    if (0 === i) {
      const segmentLength = avgSize - 2 + firstPad - (chunkSize < 10 ? 1 : 2);
      out +=
        "[" +
        String(chunkSize) +
        Array(segmentLength).fill(lineChar).join("") +
        "|";
    } else if (count === i + 1) {
      out +=
        Array(avgSize - 1 + lastPad)
          .fill(lineChar)
          .join("") + "]";
    } else {
      out +=
        Array(avgSize - 1)
          .fill(lineChar)
          .join("") + "|";
    }
  }
  return out;
}

function printSheetForToday() {
  console.log(`[=]${moment().format("ddd MMM D, YYYY")}`);
  for (const task of prepareChecklist()) {
    console.log(
      `<=>${task.label} (${getHumanReadableDuration(task.duration)})`
    );
    const bar = printBar(task.duration);
    console.log(bar);
    console.log("");
  }
}

printSheetForToday();

