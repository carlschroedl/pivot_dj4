# Pivot Django Prototype

This is a prototype rewrite of [Pivot](https://github.com/pivot-libre/pivot).

## Setup

### Install
* git
* python 3
* poetry

### Setup
Clone the repo, `cd` into the cloned directory.

```bash
# Create virtualenv, install dependencies into it
$ poetry install
# Activate virtualenv, use installed dependencies
$ poetry shell
# Apply database migrations
$ python manage.py migrate
# Create a poll programatically (no UI for this yet)
$ python manage.py shell
from polls.models import Poll
Poll(name='Favorite Letters', text='Rank your favorite letters').save()
exit()
# Run the web app
$ python manage.py runserver
```

* Visit http://127.0.0.1:8000/polls

When you want to stop the app, return to the terminal and press Ctrl+C