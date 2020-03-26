# **Behavioral Cloning** 

## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./writeup_images/straight.jpg "Straight road center driving"
[image2]: ./writeup_images/recover_mud_1.jpg "Recovery from muddy section 1"
[image3]: ./writeup_images/recover_mud_2.jpg "Recovery from muddy section 2"
[image4]: ./writeup_images/recover_sharp_1.jpg "Recovery from sharp turn 1"
[image5]: ./writeup_images/recover_sharp_2.jpg "Recovery from sharp turn 2"

## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
### Files Submitted & Code Quality

#### 1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network
* video.mp4 which is a video of a lap using model.h5
* writeup.md summarizing the results

#### 2. Submission includes functional code
Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track by executing 
```sh
python drive.py model.h5
```

#### 3. Submission code is usable and readable

The runfile.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works. 

### Model Architecture and Training Strategy

#### 1. An appropriate model architecture has been employed

My model consists of 2 convolution neural network layers with 5x5 filter sizes and depth 6.These are followed by their respective RELU activations and then a Max Pooling Layer.

Since the goal of the project was to correlate the steering angle with the lines of the road, having too many high level layers might cause it to overfit. 

Therefore, only one fully connected layer of length 120 is used.

#### 2. Attempts to reduce overfitting in the model

The model contained dropout layers initially. But their effectiveness in overfitting was similar to removing the fully connected layers altogether.

#### 3. Model parameter tuning

The model used an adam optimizer, so the learning rate was not tuned manually.

#### 4. Appropriate training data

Training data was chosen to keep the vehicle driving on the road. I used a combination of center lane driving, recovering from the left and right sides of the road and counterclockwise lap of the track. This also partly took care of the performance on the sharp turns and their recovery from them.

For details about how I created the training data, see the next section. 

### Model Architecture and Training Strategy

#### 1. Solution Design Approach

The overall strategy for deriving a model architecture was to make sure the low level features like lines and curves are given more importance than the combined higher-level features.

My first step was to use a convolution neural network model similar to the LeNet architecture. I thought this model might be appropriate because it had the layers of convolution network at the beginning and fully connected layers only at the end which ensured clear segregation in higher level and lower level features.

In order to gauge how well the model was working, I split my image and steering angle data into a training and validation set. I found that my first model had a low mean squared error on the training set but a high mean squared error on the validation set. This implied that the model was overfitting. 


To combat the overfitting, I modified the model so that there were more dropout layers. However, I did not want to include these dropout layers in the validation set too. Thus I removed them completely and tried removing the fully connected layers. I also removed an initial conv2d layer(3rd) which might not be necessary.

These steps ensure that the Validation loss was not greater than the training loss.

The final step was to run the simulator to see how well the car was driving around track one. There were a few spots where the vehicle fell off the track, specifically the muddy section at the end of the bridge. To improve the driving behavior in these cases, I collected multiple recovery datasets throughout the track and this spot.

At the end of the process, the vehicle is able to drive autonomously around the track without leaving the road.

#### 2. Final Model Architecture

The final model architecture (model.py lines 49-59) consisted of a convolution neural network with the following layers and layer sizes
1. 2D Convolutional layer (filter size = 5\*5,Number of filters = 6)
2. Max pooling Layer
3. 2D Convolutional layer (filter size = 5\*5,Number of filters = 6)
4. Max pooling Layer
5. Fully Connected layer length 120
6. Final layer with single label output for steering


#### 3. Creation of the Training Set & Training Process

To capture good driving behavior, I first recorded two laps on track one using center lane driving. Here is an example image of center lane driving:

![alt text][image1]

I then recorded the vehicle recovering from the left side and right sides of the road back to center so that the vehicle would not drive off the road at the slightest offset. These images show what a recovery looks like :

![alt text][image2]
![alt text][image3]
![alt text][image4]
![alt text][image5]

Then I repeated this process on track two in order to get more data points.

To augment the data sat, I also flipped images and angles thinking that this would account for additional data on the same section of the road.


After the collection process, I had ~4500 number of data points. I then preprocessed this data by flipping it which doubled its size.


I finally randomly shuffled the data set and put 20% of the data into a validation set. 

I used this training data for training the model. The validation set helped determine if the model was over or underfitting. The ideal number of epochs was 4 as evidenced by the rising validation loss. I used an adam optimizer so that manually training the learning rate wasn't necessary.
