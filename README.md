# ico-drf-token

create a heroku app
```heroku create```
and it would output the name of our app, in my own case
afternoon-scrubland-88520

Add the `SECRET_KEY` environment variable
```heroku config:set SECRET_KEY=SOME_SECRET_VALUE -a afternoon-scrubland-88520```

There are many ways to deploy on heroku, but i will be going with the build manifest method.

Set the Stack of your app to container:
```heroku stack:set container -a afternoon-scrubland-88520```

Install the heroku-manifest plugin from the beta CLI channel
```
heroku update beta
heroku plugins:install @heroku-cli/plugin-manifest
```

Add the Heroku remote from your initialised repo
```heroku git:remote -a afternoon-scrubland-88520```

Push the code up to Heroku to build the image and run the container:
```git push heroku HEAD:master```

##Postgres

Create the database
```heroku addons:create heroku-postgresql:hobby-dev -a afternoon-scrubland-88520```

Once the database is up, run the migrations
```
heroku run python manage.py makemigrations -a afternoon-scrubland-88520
heroku run python manage.py migrate -a afternoon-scrubland-88520
```

Populate the database too
```heroku run python manage.py populate_site -a afternoon-scrubland-88520```

