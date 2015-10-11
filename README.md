# theTrack
theTrack is a Flask application that tries to find the "best" track of an artist (according to Soundcloud users).

<img src="http://piqoni.github.io/assets/thetrack.png"/>

Application demo: http://thetrack.pythonanywhere.com/ 

## Installation
### Install requirements

```pip install -r requirements.txt```

### Soundcloud API credentials
Sign up (if not already) on [soundcloud.com](http://www.soundcloud.com) and go to http://soundcloud.com/you/apps to register a new application.
Then, get your Client ID and create a file in project root called **credentials.py** with a variable called *id* holding your Client ID string.

```python
# API credential
id='YOUR_CLIENT_ID'
```

## Features / TODO

* :white_check_mark: Search by artist name and get the best track
* :white_check_mark: Searbh by artist soundcloud URL
* :x: Suggest similar artists 