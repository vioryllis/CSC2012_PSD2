# CSC2012_PSD2

## remember to make your own venv
> "C:\Users\USER\AppData\Local\Programs\Python\Python310\python.exe" -m venv venv<br />
> or<br />
> python -m venv venv

##  remember to pip install django

> run 'python manage.py startapp app_name' to create the app

### should create a different branch for each microservice we have
> Data Ingestion + Sensor Management Service: Retrieve data and display real-time visualisation<br />
Data Processing Service: Display sensor data history, Gain more insights on the data<br />
Crop Yield Prediction Service: Use model to do some predictions<br />
User Interface Service

### to run the server
If running locally, edit the following code in ```settings.py``` file to match your database settings:
```
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': 'farawayfarmer', # database name
        'USER': 'example',
        'PASSWORD': 'example',
        'HOST': 'db',
        #'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
```
python manage.py migrate
```
```
python manage.py runserver
```


### to run docker container
From the root directory, run
```
docker-compose up
```
# end
