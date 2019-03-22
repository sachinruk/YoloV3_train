while getopts ":o:" opt; do
  case $opt in
    o) arg1="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

CAT_DIR=$PWD
mkdir weights # to store weights as training progresses
# create class names file
echo $arg1>>classes.names
# get Data and split into training and testing
python getData.py --cat $arg1
python splitTrainTest.py $PWD/JPEGImages

# clone the darknet (yolo repo)
git clone https://github.com/pjreddie/darknet
mv ./Makefile darknet/Makefile #replace makefile with GPU option mkfile
cd darknet
make

# download the yolov3 weights
curl https://pjreddie.com/media/files/darknet53.conv.74 --output darknet53.conv.74

./darknet detector train $CAT_DIR/darknet.data  $CAT_DIR/darknet-yolov3.cfg ./darknet53.conv.74 > $CAT_DIR/train.log