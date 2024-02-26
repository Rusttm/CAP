module pgsql alchemy:
update sql db from ms api
1. Hourly updates: update
2. daily updates: update
3. ondemand updates: update


Database installation
from https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart#step-2-using-postgresql-roles-and-databases
or
from https://dev.to/rainbowhat/postgresql-16-installation-on-ubuntu-2204-51ia

1. $ sudo apt install postgresql postgresql-contrib
   1.1 sudo apt install postgresql-16 postgresql-contrib-16
2. $ sudo systemctl start postgresql.service
3. $ psql --version
4. $ sudo -i -u postgres
5. postgres@rusttm-msi:~$ createuser --interactive
   if you need to change pass 
   4.1 $ sudo -u sammy psql
   4.2 postgres=# ALTER ROLE cap_user WITH PASSWORD 'capuser_pass';
   
6. postgres@rusttm-msi:~$ createdb cap_db

postgres deletion
from https://askubuntu.com/questions/32730/how-to-remove-postgres-from-my-installation


$ sudo apt-get --purge remove postgresql postgresql-*
$ dpkg -l | grep postgres
