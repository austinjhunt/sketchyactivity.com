from .models import *
import datetime,json
# use this json serialization function particularly for objects with dates as fields
def json_default(value):
    if isinstance(value, datetime.datetime):
        return dict(year=value.year, month=value.month, day=value.day, hour=value.hour,min=value.minute,sec=value.second)

    elif isinstance(value, datetime.date):
        return dict(year=value.year,month=value.month,day=value.day)

    elif isinstance(value,datetime.time):
        value = value.strftime("%I:%M")
        value = datetime.datetime.strptime(value, "%H:%M")
        return dict(hour=value.hour,min=value.minute)

    else:
        return value.__dict__



