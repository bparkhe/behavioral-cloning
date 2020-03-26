import csv
from scipy import ndimage
import numpy as np
import cv2
import io

# opengint the csv file of the combined dataset
# which includes clockwise run, counterclockwise run and recovery mode images
lines = []
# combined.csv is a combination of the recovery and straight driving
# driving_log.csv is only dataset for straight driving
# for purpose of submission the data folder has been moved to /opt
with io.open('./data/combined.csv') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for line in reader:
        lines.append(line)

# paddign the image paths with the appropriate path name
images = []
measurements = []
for line in lines:
  source_path = line[0]
  filename = source_path.split('/')[-1]
  current_path = './data/IMG/' + filename
  image = ndimage.imread(current_path)
  images.append(image)
  measurement = float(line[3])
  measurements.append(measurement)

# augmenting the data set with flipped images and negative steering values
augmented_images, augmented_measurements = [],[]
for image,measurement in zip(images,measurements):
    augmented_images.append(image)
    augmented_measurements.append(measurement)
    augmented_images.append(np.fliplr(image))
    augmented_measurements.append(measurement*-1)

   
X_train = np.array(augmented_images)
y_train = np.array(augmented_measurements)

# Model architecture (similar to LeNet barring a few changes)
from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Conv2D, MaxPool2D, Cropping2D, Dropout

model = Sequential()
# normalizing the input
model.add(Lambda(lambda x: x / 127.5 - 1,input_shape=(160,320,3)))

# cropping the images to remove surrounding interference
model.add(Cropping2D(cropping=((70,25),(0,0))))
# features like shapes and lines are more important than higher levl feauter in this network
model.add(Conv2D(6,(5,5),activation='relu'))
model.add(MaxPool2D())
model.add(Conv2D(6,(5,5),activation='relu'))
model.add(MaxPool2D())
model.add(Flatten())
model.add(Dense(120))
# ommitted 2 layers 
# omitting one more dense layer also improves the performance
model.add(Dense(1))

# Training the network
model.compile(loss='mse',optimizer='adam')
model.fit(X_train,y_train,validation_split=0.2,shuffle=True,nb_epoch=4)

model.save('model.h5')
