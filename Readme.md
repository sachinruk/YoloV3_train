# YOLO Training

This script downloads darknet and trains for *one* particular class. This script is only compatible with machines that have Nvidia drivers and CUDNN installed.

## Instructions
1. `git clone https://github.com/sachinruk/YoloV3_train.git && cd ./YoloV3_train`
2. Change the password in `run.sh` file to something secure. 
3. Run `bash run.sh` and go to localhost:8888 on your browser. You may need to do port forwarding to your local machine if you are running on a remote machine. In my case when connecting to remote instance I had to do `ssh -i aws_permissions.pem -L 8001:localhost:8888 ubuntu@$instanceIp`.
4. Enter the password that is stated on the `run.sh` file (please change the default) and open up a terminal in jupyter notebooks.
5. Run `bash train.sh -o snowman` for a snowman detector. All valid object types are listed under `categories.txt`.

