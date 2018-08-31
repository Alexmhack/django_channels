# django_channels
using django and web sockets to create a simple yet elegant project

# Objective
1. Create django project with support for web sockets using django channels
2. Setup a connection between django and redis server
3. Django app with basic user authentication
4. Using django signals send a message whenever a user logins

# Initial setup
1. Create virtualenv using any package, I will be using virtualenvwrapper

	```
	> mkvirtualenv channels
	> workon channels
	(channels)> deactivate
	> 
	```
2. Installing django, channels, asgi redis

	```
	(channels)> pip install django channels asgi_redis
	```

3. Starting project
	
	```
	(channels)> django-admin startproject channel_dj .
	(channels)> python manage.py runserver
	```

4. Creating app

	```
	(channels)> python manage.py startapp display
	```

5. Running migrations

	```
	(channels)> python manage.py migrate
	(channels)> python manage.py runserver
	```

# Errors
On installing channels package from pip I got an error saying 

```
building 'twisted.test.raiser' extension
    error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build 
    Tools": https://visualstudio.microsoft.com/downloads/
```

I solved this problem by installing channels outside of my virtualenv.
