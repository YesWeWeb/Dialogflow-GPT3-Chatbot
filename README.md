To find logs, type:
heroku logs --tail -a solomon


To push:
git push origin master


To run terminal on heroku:
heroku run bash -a solomon


To check only errors:
heroku logs --tail | grep "error"


after git push heroku should work, it will run app.py on port 80 automatically, using Procfile gunicorn command