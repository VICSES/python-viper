# Synopsis



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


