del *.db
del *.pyc
del *.log

python database_setup.py

python database_import.py

python single_database_update.py

python continuous_database_update.py
