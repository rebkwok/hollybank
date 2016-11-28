[![Build Status](https://travis-ci.org/rebkwok/hollybank.svg?branch=master)](https://travis-ci.org/rebkwok/hollybank)
[![Coverage Status](https://coveralls.io/repos/rebkwok/hollybank/badge.svg)](https://coveralls.io/r/rebkwok/hollybank)


# Online banking for Holly

# Local development

Vagrant provisioning requires ansible 2.1.1.0 AND python 2.7

# Required settings

- SECRET_KEY: app secret key
- DATABASE_URL: database settings
- LOG_FOLDER: path to folder containing the app's log files
- EMAIL_HOST_PASSWORD: password for emails sent from the app

# Optional for dev
- USE_MAILCATCHER: Boolean, set to True to send mail to mailcatcher
- DEBUG: False for dev

