import datetime

def print_date(date):
    print(date.strftime("%b %d %Y"))

today = datetime.datetime.today()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)

print_date(yesterday)
print_date(today)
print_date(tomorrow)
