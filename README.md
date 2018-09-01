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

# Project
Add channels and our display app in the project settings

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'display',
]
```

Configure the CHANNEL_LAYERS by setting a default backend and routing

Running the ubuntu app on windows 10 install the app from windows store and run the command

**cmd**
```
C:/users/--/--> ubuntu1804 
```

**Start redis server**

**Ubuntu1804 on windows 10**
```
$ sudo apt-get install redis-server
$ redis-server
```

If the redis-server command shows error saying port already in use you can run,

**Ubuntu1804**
```
$ redis-cli shutdown
$ redis-server
```

# Creating Consumers
Create a file named consumers.py in the display app which will handle the basic connection 
between the client and server

```
from channels import Group

def ws_connect(message):
	Group('users').add(message.reply_channel)
```

Any user connecting to our app will be added to the users group and will receive message sent
by the server.

```
def ws_disconnect(message):
	Group('users').discard(message.reply_channel)
```

Any users if disconnects from the app will be removed from the users group and the user will 
stop receiving messages.

# Creating Routes
We will setup routes the same way django uses urls by creating a new file in main project
folder named *routes.py*

**channel_dj/routes.py**
```
from channels.routing import route
from display.consumers import ws_connect, ws_disconnect


channel_routing = [
	route('websocket.connect', ws_connect),
	route('websocket.disconnect', ws_disconnect)
]
```

We have defined channel_routing instead of url_patterns and route() instead of path() and we
have connected our consumer functions to websockets.

In our user_list.html template we have a block tag for our javascript code which simply 
uses the WebSocket instance and prints a message whenever a new socket connection is opened.

**templates/display/user_list.html**
```
<script type="text/javascript">
	var socket = new Websocket('ws://' + window.location.host + '/users/');
	socket.onopen = function open() {
		console.log("WEBSOCKET CONNECTION CREATED");
	}

	if (socket.readyState == WebSocket.OPEN) {
		socket.onopen();
	}
</script>
```

on socket open we call a function which prints a message.

# Views & Urls
In this section we setup a django views to render our template using our display app views

**display/views.py**
```
from django.shortcuts import render


def user_list(request):
	return render(request, 'display/user_list.html')
```

**display/urls.py**
```
from django.urls import path

from .views import user_list

urlpatterns = [
	path('', user_list, name='user-list'),
]
```

Now add url for display app in main project urls

**channels_jd/urls.py**
```
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('display.urls', namespace='display')),
]
```

Namespace avoid same name collisions when your project has a lot of apps with a lot of views

# Changes in [channels version 2](https://channels.readthedocs.io/en/latest/one-to-two.html)
Settings are still similar to before, but there is no longer a ROUTING key (the base routing 
is instead defined with ASGI_APPLICATION):

**project/settings.py**
```
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis-server-name", 6379)],
        },
    },
}
```

Function based views no longer exists and you have to use the class based views
Refer to the docs or the use the channels official [tutorial](https://channels.readthedocs.io
/en/latest/tutorial/part_1.html)
