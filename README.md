# habitica-webhooks

# Purpose

The productivity app Habitica keeps a log of actions, but only returns the data summed by day. There is no way to, for example, see a list of actions along with the time of day they were logged. Furthermore, Habitica separates the days by UTC time, which means that actions taken on the same day (local time) may show up on different days in the log.

To address this problem, this Flask app is designed to be run on Heroku and receive webhook triggers whenever a task is logged, and to create a database of actions along with their time and date in local time.

# Heroku setup

1. Fork this repository
2. Connect your Github account to your Heroku account
3. In Heroku, create a Postgres database (in the Addons options)
4. In Heroku, add the Postgres DB url and your time zone to the Environment Variables (in Settings)
It should look like:
  DATABASE_URL – postgres://{YOUR URL HERE}
  TZ – "America/New_York"
5. Set up a webhook connection using [this site](https://robwhitaker.com/habitica-webhook-editor/).

TODO: finish this
