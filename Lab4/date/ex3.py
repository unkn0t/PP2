import datetime

def drop_micros(dt: datetime.datetime):
    dt.replace(microsecond=0)

now = datetime.datetime.now()
print(now)
now -= datetime.timedelta(microseconds=now.microsecond)
print(now)
