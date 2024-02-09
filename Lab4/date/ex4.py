import datetime as dt

def diff(dt1: dt.datetime, dt2: dt.datetime):
    return (dt2 - dt1).total_seconds() 

today = dt.datetime.today()
before = dt.datetime(year=2020, month=1, day=22)
print(diff(before, today))

