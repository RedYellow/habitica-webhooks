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
    - DATABASE_URL – postgres://{YOUR-DB-URL-HERE}
    - TZ – America/New_York
      - Do not put quotes in here
    - If running this locally as a test, export these as environment variables in the command line
5. Set up a webhook connection using the [Habitica webhook editor](https://robwhitaker.com/habitica-webhook-editor/)
    - Your user ID and API token are available in your Habitica account settings
    - **Make sure that the URL given is the `/webhook` endpoint (e.g. https://{YOUR-APP-URL}.herokuapp.com/webhook)**. This is the only place that can receive the webhook triggers.
    - Note that you must set up a separate webhook for each type of data (e.g. taskActivity, userActivity,...)

# Warnings

- If a webhook fails 10 times in one month, it will be disabled. This happens on the Habitica side, not this app.
    - If you go to the webhook editor and a webhook appears greyed out, it is disabled.
- If a webhook fails to be logged in the database (e.g. if you deployed a build that has a bug), there is no way to get the data back.
    
# Use

This is designed to be mostly-hands off, and as such it doesn't have a lot of interactability. The main page displays a summary of your data, and the full data in json form can be accessed at the `/getall` endpoint.

To download the json data, you can run something like: `curl https://{YOUR-APP-URL}.herokuapp.com/getall  -o ~/Downloads/habitica_data.json`

# Testing

You might want to test the app before you run it in Heroku, which you can do in the way of a regular Flask app. However, you will need to install Postgres and create a local database in order to do so. Be sure to call it "habitica_db", or change the URL in the .flaskenv file.

You can run a command like this to send webhook triggers to your local app: 

  `curl -X POST -H 'Content-type: application/json' --data '{
          "message": "Your egg hatched! Visit your stable to equip your pet.",
          "pet": "TigerCub-Shade",
          "type": "petHatched",
          "user": {
              "_id": "id"
          },
         "webhookType": "userActivity"
      }' http://localhost:5000/webhook`
