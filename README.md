[![Build Status](https://travis-ci.org/VICSES/python-viper.svg?branch=master)](https://travis-ci.org/VICSES/python-viper)
[![Coverage Status](https://coveralls.io/repos/github/VICSES/python-viper/badge.svg?branch=master)](https://coveralls.io/github/VICSES/python-viper?branch=master)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FVICSES%2Fpython-viper.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FVICSES%2Fpython-viper?ref=badge_shield)

# Synopsis

```python
from vicses.viper import Viper

viper = Viper(ses_id='123', ses_password='password')
viper.send('12345', 'This is the contents of an admin page')
```


# Python library to access VICSES Viper program

To send messages on the Emergency Alerting System (EAS) pager network the
Victoria State Emergency Service runs an online program called Viper.
Viper is developed and maintained by Visionsteam, a private company with
the maintenance contract for the EAS network. VICSES has very limited control.

Viper is a basic HTML serverside form based program. Functional but a little
ugly and not suitable for use as a service.

To make life a bit more exciting there is a Viper login page that must be navigated but only after climbing through the SES reverse proxy login. Both systems time out the login after a while but at different times leading to staggering.

# What

This library takes care of all the annoying login processes and form manipulation. It performs the various web requests so you can pretend you are working with a well designed API.

# Annoying details

This library was developed by a VICSES volunteer without the knowledge or support of VICSES or any VICSES staff. This is not an officially condoned program, they will provide no support, they are probably horrified that it exists.

Due to its nature this library is fragile to changes to Viper or the reverse proxy system. This library may break at any time, do not use it for mission critical tasks.

This library is licenced under the GNU Affero General Public License, the full text is included in LICENCE.md.  Feel free to use this library for your product so long as the full source code for this library and the product you use it in is made available to your users.  Please read the full licence for the details, there are also extensive explanatory articles online.

# Reference

## \_\_init\_\_

Optional parameters:

* ses\_id
* ses\_username
* ses\_password
* viper\_username
* viper\_password

Init must be able to set a value to all the username and password fields. If provided with an ses\_id number it will use it to generate the default values for ses\_username, viper\_username and viper\_password.

## send

Required parameters:

* to
* msg

Optional parameters:

* priority

This sends a page to the pager number supplied in the to field. The msg field contains the body of the message.

Priority is a number between 1 and 3. 1 sends an emergency message, 2 sends a non-emergency message and 3 sends an administrative message. If not specified priority defaults to 3. Most users only have permission to send administrative messages.

Send returns an error value.
On success it will return False.
On failure it will return the element that it got stuck on, one of "SES Login", "Viper Login", or "Unknown response"

## logging

This module uses the logging library. Extensive output is provided if turned up to DEBUG, including the full output of every server response.


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FVICSES%2Fpython-viper.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FVICSES%2Fpython-viper?ref=badge_large)