Hello, and thanks for downloading HeroArchitect! This document serves as an installation guide.

WARNING: This project utilises PostgreSQL for database management. Installing and configuring this correctly may prove
challenging. Additionally, you will need to execute a script in order to populate the database with prerequisite data
required for HeroArchitect to run properly. I have authored the script to the best of my ability and tested it on my
own machine, and so I can only apologise if this script does not work.

Steps to install HeroArchitect are as follows:

1. Ensure that you have Python 3 and pip installed on your machine, and correctly configured with your machine's
PATH variables:
- Python3: https://www.python.org/downloads/
- pip: https://pypi.org/project/pip/

2. Open a command terminal, and use the cd command to navigate to the /heroArchitect/ directory (the directory that you
found this txt file in). Then, install the Python dependencies using "pip install -r requirements.txt".

3. Install pgAdmin 4, the PostgreSQL database manager: https://www.pgadmin.org/download/pgadmin-4-windows/ (this link
is for windows; navigate to macOS/linux download pages as necessary).

4. Once installed, open pgAdmin 4, create a super-user account, and record the login details.

5. Also inside pgAdmin 4, create a database. Assign the name of the database to be anything of your choosing, and assign
the owner of the database to be the super-user account you created in step 4.

6. Close pgAdmin 4, and navigate to /heroArchitect/heroArchitect/settings.py in a file explorer. Locate the DATABASES configurable (around line 100). Enter the database name from step 5, and the super-user details from step 4.

7. Again in the command terminal, in the /heroArchitect/ directory, create and apply database model migrations by
using the following commands:
    i. 'python manage.py makemigrations'
    ii. 'python manage.py migrate'

8. Execute database_initialiser.py (can be found in the /heroArchitect/ directory).

9. In the command line, in the /heroArchitect/ directory, execute 'python manage.py runserver', and navigate to 127.0.0.1
in any web browser of your choice. Assuming all preceeding steps have been executed without issue, you should now have
access to the latest development version of HeroArchitect!

If you have performed all of the above steps and issues still persist, please consult this informative guide:
https://www.youtube.com/watch?v=unFGJhIvHU4

If there is an error in the database_initialiser.py script, feel free to reach out to me at nm548@exeter.ac.uk. The
development environment is frustrating to replicate on other machines, and for that, I can only apologise!