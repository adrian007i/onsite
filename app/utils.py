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

def is_empty(value): 

    if value is None:
        return True
    if isinstance(value, str) and value.strip() == "":
        return True 
    return False    

error_messages =  {
    'unique': 'This email is already registered.',
    'invalid': 'Invalid',
    'invalid_choice': 'Invalid',
    'null': 'Required',
    'blank': 'Required',
} 