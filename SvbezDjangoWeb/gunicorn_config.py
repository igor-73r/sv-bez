command = '/home/projects/svbez/venv/bin/gunicorn'
pythonpath = '/home/projects/svbez/SvbezDjangoWeb'
bind = '127.0.0.1:8001'
workers = 3
user = 'svbez'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=SvbezDjangoWeb.settings'
