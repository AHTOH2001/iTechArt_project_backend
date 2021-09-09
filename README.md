# Django backend of the iTechArt internship project

## Deployment manual

- Clone this repository
- Optionally run command `git checkout develop` if you want to launch develop version of the backend
- Run command `python -m venv venv` to create virtual environment
- Activate virtual environment
    - On Windows run command `venv\Scripts\activate.bat`
    - On Unix run command `source venv\Scripts\activate`
- Run command `pip install -r requirements.txt` to install necessary packages
- Somehow contact with the developer to get the secret key. Secret key will be in .env file that you need to put in the
  root folder of the project.
- That is it, now you can run any django command, for an example you can run command `python manage.py migrate` to
  create sqlite database, create super user using command `python manage.py createsuperuser` and then run development
  server using command `python manage.py runserver` and so on.
