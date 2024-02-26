#from https://habr.com/ru/articles/659813/

$ sudo ufw allow 2376
$ sudo ufw allow 2377
$ sudo ufw allow 7946
$ sudo ufw allow 7946:7946/udp
$ sudo ufw allow 4789


$ sudo docker swarm init --advertise-addr 192.168.50.175
$ sudo docker stack deploy --compose-file docker-compose.yml postgres-swarm

# from https://stackoverflow.com/questions/38249434/docker-postgres-failed-to-bind-tcp-0-0-0-05432-address-already-in-use
# who uses the port?
# $ sudo ss -lptn 'sport = :5432'
