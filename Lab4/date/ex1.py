import datetime

today = datetime.datetime.today()
print("Today:", today)

five_days_ago = today - datetime.timedelta(days=5)
print("Five days ago:", five_days_ago) 
