## Django App

For windows, replace any `python3` reference with `py -3`


```

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver

```

- Django serves to http://127.0.0.1:8000/ by default
- To access the admin console, use `python3 manage.py createsuperuser`
- _makemigrations_ creates (but does not apply) the migrations
- _migrate_ command actually applies the migrations to your database
- `python manage.py migrate captioner zero` will reset all migrations and start over
- `python manage.py flush` will clear tables out (but not delete the tables sooooo yeahhhhh)