IMAGE_ID=pristine70/receptionbot:0.1
NAME_ID=pristine70_receptionbot
#IMAGE_ID=pristine70/python3
#NAME_ID=pristine70_python3
DOCKER=docker

$DOCKER run -it --rm \
   --name $NAME_ID \
   --device /dev/snd \
   -p 22345:5000 \
   -v $(pwd):/receptionbot $IMAGE_ID \
   /bin/bash

#$DOCKER run -it --rm \
#   --name $NAME_ID \
#   -p 8080:5000 \
#   -v $(pwd):/python-docker $IMAGE_ID
