nvidia-docker run -d -p 8888:8888 -p 6006:6006 --shm-size 50G -e PASSWORD=RickAndMorty -v ${PWD}:/notebook -v ${PWD}/data/:/notebook/data sachinruk/pytorch_gpu
