
docker build -t matplotlib -f config/matplotlib.Dockerfile .
docker run --privileged -ti -v ${PWD}:/usr/local/bin/matplotlib -p 8888:8888 matplotlib