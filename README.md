# Pokemon Alert

Automatic search pokemon in FPM using python and webdriver, sending email when it encounters.

### Install Dependecies

I only tested on Linux, but running on windows should not be a problem.

First, you need install Chrome Driver:
> https://sites.google.com/a/chromium.org/chromedriver/getting-started
> http://chromedriver.storage.googleapis.com/index.html?path=2.25/

Install Python 2.7:
> https://www.python.org/downloads/

Install requered python packaged (use with virtualenv):
> pip install -r requirements.txt

Create this folders in home dir (~/.pokemon/ and ~/.pokemon/logs):
> mkdir -p ~/.pokemon/logs

In ~/.pokemon create config.json and puts your email info:

```json
{
	"global": {
		"email": {
			"from": "mail@mail.com",
			"password": "emailpassword",
			"maps-key": "mapskey",
			"to": [
				"iwantpokemon@mail.com"
			]
		}
	},
	"places": {
		"university": {
			"latitude": "-23.123456",
			"longitude": "-51.123456"
		},
		"park": {
			"latitude": "-23.426085",
			"longitude": "-51.9397617"
		},
		"myhome": {
			"latitude": "-23.123456",
			"longitude": "-51.123456"
		}
	}
}
```

### Usage

> python main.py <place>
> ex: python main.py university

### TODO:
Move search pokemon names to config.json
