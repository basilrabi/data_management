import datetime
import pytz

# AutoCAD Color Index (ACI) assigned for each ore class
ACI = {
    'A': 1,
    'B': 2,
    'C': 5,
    'D': 32,
    'E': 8,
    'F': 7,
    'L': 3,
    'W': 6
}

one_day = datetime.timedelta(days=1)
one_hour = datetime.timedelta(hours=1)
one_minute = datetime.timedelta(minutes=1)
one_second = datetime.timedelta(seconds=1)
tz_manila = pytz.timezone('Asia/Manila')
zero_time = datetime.timedelta()
