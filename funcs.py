from datetime import datetime, timedelta


def convert_time(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    if hours >= 24:
        hours -= 24
        new_date = datetime.now() + timedelta(days=1)
    else:
        new_date = datetime.now()
    new_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    new_time_obj = datetime.strptime(new_time_str, '%H:%M:%S')
    return new_date.replace(hour=new_time_obj.hour, minute=new_time_obj.minute, second=new_time_obj.second)