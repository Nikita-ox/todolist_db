#!/bin/bash
ls -lah
cd todolist
python manage.py migrate --check
status=$?
if [[ $status != 0 ]]; then
  python manage.py migrate
fi
cd ..
exec "$@"