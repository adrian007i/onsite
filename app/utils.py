import datetime

def formatNumber(value):

    try:
        int(value)
        return int(value)
    except ValueError:
        return None
    
def formatDate(value): 

    date_format = '%Y-%m-%d'
 
    try: 
        dateObject = datetime.datetime.strptime(value, date_format)
        return value
    except ValueError:
        return None
            