
import sys, os, django, random
from django.core.management.color import no_style
from django.db import connection

# IMPORT DJANGO SETTINGS CONFIG
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'onsite_jobs.settings' 
 
django.setup()
 
# IMPORT DATABASE MODEL
from app.models.user import User
  
# DELETE ALL THE EXISTING DATA
User.objects.all().delete() 

# RESETS THE SEQUENCE IN CERTAIN DATABASES LIKE MYSQL MSSQL
sequence_sql = connection.ops.sequence_reset_sql(no_style(), [User]) 
with connection.cursor() as cursor:
    for sql in sequence_sql:
        cursor.execute(sql)

# RESETS THE SEQUENCE IN SQLLITE
with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = 'app_user';")
 
   

with connection.cursor() as cursor:
    cursor.execute(
        f"""
            INSERT INTO app_user ("password", "last_login", "email", "other_headline", "company", "first_name", "last_name", "is_active", "is_superuser", "is_staff", "date_joined", "role", "headline_id", "location_id") 
            VALUES 
            ('pbkdf2_sha256$870000$saSCga85TuLgX9BY8B0zZl$kklXL3poveFRDoFInEuh57cZXc4eGdujjLTWr8eTQBU=', '2024-11-02 12:36:56.513762', 'sarah.thomas@helionix.com', NULL, 'Helionix', 'Sarah', 'Thomas', 1, 0, 1, '2024-11-02 12:36:56.459579', 'recruiter', 1014, { random.randrange(3576, 3627)}),
            ('pbkdf2_sha256$870000$saSCga85TuLgX9BY8B0zZl$kklXL3poveFRDoFInEuh57cZXc4eGdujjLTWr8eTQBU=', '2024-11-02 13:25:18.234546', 'jackson.reed@cybercore.com', NULL, 'Cybercore', 'Jackson', 'Reed', 1, 0, 1, '2024-11-02 13:25:18.234546', 'recruiter', 1014, { random.randrange(3576, 3627)}),
            ('pbkdf2_sha256$870000$saSCga85TuLgX9BY8B0zZl$kklXL3poveFRDoFInEuh57cZXc4eGdujjLTWr8eTQBU=', '2024-11-02 09:12:34.123456', 'lisa.martin@vergecorp.com', NULL, 'VergeCorp', 'Lisa', 'Martin', 1, 0, 1, '2024-11-02 09:12:34.123456', 'recruiter', 1014, { random.randrange(3576, 3627)}),
            ('pbkdf2_sha256$870000$saSCga85TuLgX9BY8B0zZl$kklXL3poveFRDoFInEuh57cZXc4eGdujjLTWr8eTQBU=', '2024-11-02 15:34:56.654321', 'michael.green@infiniwave.com', NULL, 'Infiniwave', 'Michael', 'Green', 1, 0, 1, '2024-11-02 15:34:56.654321', 'recruiter', 1014, { random.randrange(3576, 3627)}),
            ('pbkdf2_sha256$870000$saSCga85TuLgX9BY8B0zZl$kklXL3poveFRDoFInEuh57cZXc4eGdujjLTWr8eTQBU=', '2024-11-02 14:02:43.876543', 'emma.lee@novabyte.com', NULL, 'NovaByte', 'Emma', 'Lee', 1, 0, 1, '2024-11-02 14:02:43.876543', 'recruiter', 1014, { random.randrange(3576, 3627)}),
            ('pbkdf2_sha256$870000$saSCga85TuLgX9BY8B0zZl$kklXL3poveFRDoFInEuh57cZXc4eGdujjLTWr8eTQBU=', '2024-11-02 08:46:52.321457', 'olivia.brown@optilink.com', NULL, 'Optilink', 'Olivia', 'Brown', 1, 0, 1, '2024-11-02 08:46:52.321457', 'recruiter', 1014, { random.randrange(3576, 3627)}),
            ('pbkdf2_sha256$870000$saSCga85TuLgX9BY8B0zZl$kklXL3poveFRDoFInEuh57cZXc4eGdujjLTWr8eTQBU=', '2024-11-02 11:27:09.123987', 'noah.james@tekbase.com', NULL, 'TekBase', 'Noah', 'James', 1, 0, 1, '2024-11-02 11:27:09.123987', 'recruiter', 1014, { random.randrange(3576, 3627)}),
            ('pbkdf2_sha256$870000$saSCga85TuLgX9BY8B0zZl$kklXL3poveFRDoFInEuh57cZXc4eGdujjLTWr8eTQBU=', '2024-11-02 10:15:16.555111', 'mia.jones@futuretech.com', NULL, 'FutureTech', 'Mia', 'Jones', 1, 0, 1, '2024-11-02 10:15:16.555111', 'recruiter', 1014, { random.randrange(3576, 3627)}),
            ('pbkdf2_sha256$870000$saSCga85TuLgX9BY8B0zZl$kklXL3poveFRDoFInEuh57cZXc4eGdujjLTWr8eTQBU=', '2024-11-02 09:04:23.876532', 'ethan.miller@genesisworld.com', NULL, 'GenesisWorld', 'Ethan', 'Miller', 1, 0, 1, '2024-11-02 09:04:23.876532', 'recruiter', 1014, { random.randrange(3576, 3627)}),
            ('pbkdf2_sha256$870000$saSCga85TuLgX9BY8B0zZl$kklXL3poveFRDoFInEuh57cZXc4eGdujjLTWr8eTQBU=', '2024-11-02 16:37:12.654234', 'amelia.wood@integrax.com', NULL, 'IntegraX', 'Amelia', 'Wood', 1, 0, 1, '2024-11-02 16:37:12.654234', 'recruiter', 1014, { random.randrange(3576, 3627)})
        """
    )
 