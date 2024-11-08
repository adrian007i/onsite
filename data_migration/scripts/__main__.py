response = input("This action permanently deletes ALL data in the database\nAre you sure you want to proceed? (yes/no)").strip().lower()

if response == 'yes':
    print("------------ DATABASE SEEDING BEGIN ------------")

    print("____________ DEPARTMENTS BEGIN _________________")
    import Departments
    print("____________ DEPARTMENTS END ___________________")

    print("____________ JOB TITLES BEGIN __________________")
    import JobTitles
    print("____________ JOB TITLES END ____________________")

    print("____________ LOCATIONS BEGIN ___________________")
    import Locations
    print("____________ LOCATIONS END _____________________")

    print("____________ USERS BEGIN __________________")
    import Users
    print("____________ USERS END ____________________")

    print("____________ JOBS BEGIN ___________________")
    import Jobs
    print("____________ JOBS END _____________________")

    print("------------ DATABASE SEEDING END ------------")
else:
    print('Seeding canceled!')