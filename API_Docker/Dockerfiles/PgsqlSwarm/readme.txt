#from https://habr.com/ru/articles/659813/

$ sudo ufw allow 2376
$ sudo ufw allow 2377
$ sudo ufw allow 7946
$ sudo ufw allow 7946:7946/udp
$ sudo ufw allow 4789


$ sudo docker swarm init --advertise-addr 192.168.50.175
$ sudo docker stack deploy --compose-file docker-compose.yml postgres-swarm