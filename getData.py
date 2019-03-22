import pandas as pd
import subprocess
import os
import argparse

MAX_IMAGES = 10000
LABEL_FOLDER = "./labels/" 
IMAGE_FOLDER = "./JPEGImages/"
os.makedirs(LABEL_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

df1 = pd.read_csv('./data/class-descriptions-boxable.csv', 
                  header=None,
                  names=['LabelName','Category'])
df1.Category = df1.Category.str.lower()

df2 = pd.read_csv('./data/train-annotations-bbox.csv')

parser = argparse.ArgumentParser()
parser.add_argument('--cat', help='object category', type=str)
args = parser.parse_args()
cat = args.cat.lower()

# create a data frame that contains only the required category
cat_id = df1[df1.Category.str.contains(cat)].LabelName.values[0]
cat_df = df2[df2.LabelName==cat_id]
print('Number of pictures for this category:', cat_df.ImageID.nunique())
# store only, centre of image and width, heigtht along with image Id
cat_df['x_c'] = cat_df[['XMin', 'XMax']].mean(axis=1)
cat_df['y_c'] = cat_df[['YMin', 'YMax']].mean(axis=1)
cat_df['w'] = cat_df.XMax - cat_df.XMin
cat_df['h'] = cat_df.YMax - cat_df.YMin
cat_df = cat_df[['ImageID', 'x_c', 'y_c', 'w', 'h']]

# get unique images
u_images = cat_df.ImageID.unique()
s3_cmd = 'aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/train/'

for i in range(min(len(u_images), MAX_IMAGES)):
    # download the image
    img_name = u_images[i] + '.jpg '
    dwnld_cmd = s3_cmd +  img_name + IMAGE_FOLDER + img_name
    subprocess.run(dwnld_cmd.split())

    # write down dimensions of object within image to labels folder
    dims = cat_df[cat_df.ImageID==u_images[i]].drop('ImageID', axis=1)
    with open(LABEL_FOLDER+u_images[i]+'.txt','w') as f:
        for row in dims.values:
            line = ['0'] + [str(val) for val in row]
            f.write(' '.join(line)+'\n')
            
    if (i + 1) % 100 == 0:
        print(f'Downloaded {i+1} images')