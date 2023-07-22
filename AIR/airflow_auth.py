# from https://stackoverflow.com/questions/56966292/failed-to-import-authentication-backend-after-changing-the-airflow-cfg
# pip install 'apache-airflow[password]'

import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
user = PasswordUser(models.User())
user.username = 'root'
user.email = 'new_user_email@example.com'
user.password = 'root'
session = settings.Session()
session.add(user)
session.commit()
session.close()
