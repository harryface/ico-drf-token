# ICO Token Application
Allows people to make bids, so far its within the bidding window.

At the end of a bidding window, it automatically distributes the bids according to rules below
1. Distributes to people with the larger bids first
2. When multiple people are in the same price group, gives them one first

At the end of the bid distribution, two tables would be created - for the successful bids and the unsuccessful bids.

An external API is available for prepopulating the bid window, though can only be done by an Admin user.

## Steps to Reproducing on Heroku

1. Create a heroku app
```heroku create```
and it would output the name of our app, in my own case
afternoon-scrubland-88520

2. Add the `SECRET_KEY` environment variable
```
heroku config:set SECRET_KEY=SOME_SECRET_VALUE -a afternoon-scrubland-88520
```

_There are many ways to deploy on heroku, but i will be going with the build manifest method._

3. Set the Stack of your app to container:
```
heroku stack:set container -a afternoon-scrubland-88520
```

4. Install the heroku-manifest plugin from the beta CLI channel
```
heroku update beta
heroku plugins:install @heroku-cli/plugin-manifest
```

5. Add the Heroku remote from your initialised repo
```
heroku git:remote -a afternoon-scrubland-88520
```

6. Push the code up to Heroku to build the image and run the container:
```
git push heroku HEAD:master
```

### Postgres

7. Create the database
```
heroku addons:create heroku-postgresql:dev -a afternoon-scrubland-88520
```

8. Once the database is up, run the migrations
```
heroku run python manage.py makemigrations -a afternoon-scrubland-88520
heroku run python manage.py migrate -a afternoon-scrubland-88520
```

9. Populate the database too
```
heroku run python manage.py populate_site -a afternoon-scrubland-88520
```

