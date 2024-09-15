
import csv, sys, os, django 
from pathlib import Path
from django.core.management.color import no_style
from django.db import connection

# IMPORT DJANGO SETTINGS CONFIG
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'onsite_jobs.settings' 
 
django.setup()
 
# IMPORT DATABASE MODEL
from app.models.location import Location

# SPECIFY DATA TO IMPORT
file = Path(__file__).resolve().parent.parent.joinpath("data","locations.csv") 

# OPEN FILE
data = csv.reader(open(file , encoding="utf8"), delimiter=",") 

# DELETE ALL THE EXISTING DATA
Location.objects.all().delete()

# RESETS THE SEQUENCE IN CERTAIN DATABASES LIKE MYSQL MSSQL
sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Location]) 
with connection.cursor() as cursor:
    for sql in sequence_sql:
        cursor.execute(sql)

# RESETS THE SEQUENCE IN SQLLITE
with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = 'app_location';")
 
# # INSERT THE DATA INTO THE DATABASE
for row in data:  
    location=Location()
    location.name = row[0].lower()
    location.loc_tyep = row[1]

    try:
        location.save() 
    except Exception as e:
        print(row)
        print(str(e))