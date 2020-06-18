# wireless-sleep-monitor

To run locally, create a python virtual environment with the command:
virtualenv env

launch the environment by navigating to env/Scripts and run the command activate

then install the dependencies with the command:
pip install -r requirements.txt

to run the server:
py manage.py runserver

to make model changes in the database:
Change your models (in models.py).
Run python manage.py makemigrations to create migrations for those changes
Run python manage.py migrate to apply those changes to the database.
