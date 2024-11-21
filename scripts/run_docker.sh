# to build: sudo docker build -t aioquic-earlydatatest .  # in this directory

# first time run:
sudo docker stop aioquic-earlydatatest && sudo docker rm aioquic-earlydatatest
sudo mkdir -p $(pwd)/results
sudo chmod 777 $(pwd)/results
sudo docker run -it --privileged --cap-add=NET_ADMIN -p 4433:4433/udp --name aioquic-earlydata --volume=$(pwd)/results:/srv/aioquic/qlog aioquic-earlydatatest


# after run:
# sudo docker start aioquic-earlydata # from this directory

# sudo docker exec -it aioquic-earlydata bash   # (to get back in if you would exit)