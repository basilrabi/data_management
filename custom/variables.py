from datetime import timedelta
from pytz import timezone

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

MONTH_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
    (11, '11'),
    (12, '12'),
)

one_day = timedelta(days=1)
one_hour = timedelta(hours=1)
one_minute = timedelta(minutes=1)
one_second = timedelta(seconds=1)
tz_manila = timezone('Asia/Manila')
zero_time = timedelta()
