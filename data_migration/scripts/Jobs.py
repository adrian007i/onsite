
import csv, sys, os, django ,datetime, random
from pathlib import Path
from django.core.management.color import no_style
from django.db import connection

# IMPORT DJANGO SETTINGS CONFIG
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'onsite_jobs.settings' 
 
django.setup()
 
# IMPORT DATABASE MODEL
from app.models.job import JobHead, JobDetail

# SPECIFY DATA TO IMPORT
file = Path(__file__).resolve().parent.parent.joinpath("data","locations.csv") 

# OPEN FILE
data = csv.reader(open(file , encoding="utf8"), delimiter=",") 

# DELETE ALL THE EXISTING DATA
JobHead.objects.all().delete()
JobDetail.objects.all().delete()

# RESETS THE SEQUENCE IN CERTAIN DATABASES LIKE MYSQL MSSQL
sequence_sql = connection.ops.sequence_reset_sql(no_style(), [JobHead,JobDetail]) 
with connection.cursor() as cursor:
    for sql in sequence_sql:
        cursor.execute(sql)

# RESETS THE SEQUENCE IN SQLLITE
with connection.cursor() as cursor:
    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name IN ('app_jobhead','app_jobdetail');")
  



def rand_date(year_from, year_to):
    start = datetime.date(year_from, 1, 1)
    end = datetime.date(year_to, 12, 1)
    random_date = start + (end - start) * random.random()
    return datetime.datetime.combine(random_date, datetime.datetime.min.time()).date()

# # INSERT THE DATA INTO THE DATABASE
with connection.cursor() as cursor:
        for i in range(500): 

            sal_min = random.randrange(50000,120000) 
            sal_max = sal_min + random.randrange(1,50000)
            start_date = rand_date(2023,2024)
            end_date = start_date + datetime.timedelta(days=random.randrange(15,90) )

            # job head + job detail
            cursor.executescript(f"""
            INSERT INTO "app_jobhead" ("id", "posted_on", "salary_min", "salary_max", "experience_level", "active_from", "active_to", "draft","created_by_id", "department_id", "title_id", "location_id")
            VALUES  
            ({i}, '{start_date}', {sal_min},{sal_max}, 'any','{end_date}','{rand_date(2024,2025)}', 0, { random.randrange(1, 8)},{ random.randrange(1, 28)}, { random.randrange(1, 1158)}, { random.randrange(3576, 3627)});
 
            INSERT INTO "app_jobdetail" ("id", "summary", "duties", "qualifications", "compensation", "job_head_id") VALUES  ( 
            {i},
            'A software developer is a professional who designs, builds, and maintains applications, systems, and software solutions to meet specific user needs or business requirements. Their work involves writing, testing, and debugging code, typically in programming languages like JavaScript, Python, Java, C#, and more, depending on the project requirements.', 
            '• Collaborate with product managers, team members, customers, and other engineering teams to solve our toughest problems
            • Develop and execute technical software development strategy for the organization including self-service, business continuity, backup/restores, incident response and paging platforms
            • Accountable for the quality, usability, and performance of the solutions
            • Lead projects from the front and interact with clients and sponsors on a regular basis
            • Consistently share best practices and improve processes within and across teams
            • Take on-call and operational support', 
            
            '• Advance knowledge of at least one modern OOP language such as Python or Go (preferred) Deep hands-on experience in complex system design and data pipeline and architectures, scale and performance, tuning, with good knowledge on Docker and Kubernetes
            • Strong Test-Driven Development practices (e.g., unit, functional, integration, load, etc.) In-depth knowledge of CS data structures and algorithms  Understanding of security best practices (e.g., certificates, encryption) Understand open-source databases like MySQL, PostgreSQL, etc. 
            • Familiar with No-SQL databases like Cassandra, MongoDB, etc. 
            • Experience in architecting, designing, building automation, workflows, and distributed applications
            • Strong understanding of service integrations / communication standards (e.g., GRPC / REST)
            • Experience partnering with engineering teams and transferring research to production
            • Experience with continuous delivery (CI/CD) and Infrastructure as Code
            • Experience solving analytical problems with quantitative approaches
            • Knowledge of developer tooling across the software development life cycle (task management, source code, building, deployment, test automation and related tools, operations, real-time communication)
            • Knowledge of Kubernetes, containers, and best practices on a K8s environment (including K8s operators)
            • Experience in open-source tools like GIT/Jenkin/CircleCI, and knowledge in Pulumi/Terraform/Ansible is a plus
            • Excellent communication skills
            • Ability to excel in a fast-paced, startup-like environment

            Experience:
            • 2+ years of professional experience in software development, platform architecture, administration and maintenance of software, and its ecosystem
            • 2+ years of experience with architecture and design
            • 2+ years of experience with AWS, GCP, Azure, or hybrid data center
            • 2+ years of experience in open-source frameworks

            Education:
            • Bachelor''s degree in computer science, Information Systems, or equivalent education or work experience', 
            
            'The above annual salary range is a general guideline. Multiple factors are taken into consideration to arrive at the final hourly rate/ annual salary to be offered to the selected candidate. Factors include, but are not limited to, the scope and responsibilities of the role, the selected candidate’s work experience, education and training, the work location as well as market and business considerations. As an Associate, you’ll enjoy our Total Rewards Program* to help secure your financial future and preserve your health and well-being, including:

            • Premier Medical, Dental and Vision Insurance with no waiting period**
            • Paid Vacation, Sick and Parental Leave
            • 401(k) Plan
            • Tuition Reimbursement
            • Paid Training and Licensures
            • Benefits may be different by location. Benefit eligibility requirements vary and may include length of service. 
            • Coverage begins on the date of hire. Must enroll in New Hire Benefits within 30 days of the date of hire for coverage to take effect.', {i});
            """  )
     