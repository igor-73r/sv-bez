source /home/svbez/projects/svbez/venv/bin/activate
exec gunicorn -c "/home/svbez/projects/svbez/SvbezDjangoWeb/gunicorn_config.py" SvbezDjangoWeb.wsgi
