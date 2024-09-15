
import csv, sys, os, django 
from pathlib import Path
from django.core.management.color import no_style
from django.db import connection

# IMPORT DJANGO SETTINGS CONFIG
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'onsite_jobs.settings' 
 
django.setup()
 
# IMPORT DATABASE MODEL
from app.models.job_title import JobTitle

# SPECIFY DATA TO IMPORT
file = Path(__file__).resolve().parent.parent.joinpath("data","job_titles.csv") 

# OPEN FILE
data = csv.reader(open(file), delimiter=",") 

# DELETE ALL THE EXISTING DATA
JobTitle.objects.all().delete()

# RESETS THE SEQUENCE IN CERTAIN DATABASES LIKE MYSQL MSSQL
sequence_sql = connection.ops.sequence_reset_sql(no_style(), [JobTitle]) 
with connection.cursor() as cursor:
    for sql in sequence_sql:
        cursor.execute(sql)

# RESETS THE SEQUENCE IN SQLLITE
with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = 'app_jobtitle';")
 
# # INSERT THE DATA INTO THE DATABASE
for row in data:
    jobTitle=JobTitle()
    jobTitle.name = row[0].lower()
    try:
        jobTitle.save() 
    except Exception as e:
        print(row)
        print(str(e))