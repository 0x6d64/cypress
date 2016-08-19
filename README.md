# cypress

a learning excercise in using the tweepy twitter API.

## function

Cypress connects to a twitter account and watches direct messages sent to that account. If a direct message is received from an authorized user (i.e. a user that is included in a twitter user list for that account) then cypress parses the direct messages and acts upon them.

## actions

Currently only one action is supported:
- the command "take picture" triggers a connected webcam and posts the image as a status update
- the command "delete n" deletes a status update with index n (0 being the most recent status)
- the command "say" creates a status update with the text following the command (truncated to 140 characters)

## planned features
- take picture a regular intervals for later revrieval, start and stop taking pictures by sending a command via direct message
- look for movement in image and notify users on movement

## known issues
- the size if the image uploaded is limited
- the program will most likely not fail gracefully or recover from errors (e.g. twitter being down, hitting rate limits)

## libraries used

Cypress uses [tweepy](https://tweepy.readthedocs.org/en/v3.5.0/) to connect to twitter and fswebcam to take the pictures. Handling of periodic tasks is scheduled using the [sched](https://docs.python.org/2/library/sched.html) library.
