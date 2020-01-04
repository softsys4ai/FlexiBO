<<<<<<< HEAD
#! /usr/bin/env python2.7
from __future__ import print_function
import os
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D



class Lenet(object):
    """This class is used to train Lenet
    """
    def __init__(self,
                dataset,
                n_filters,
                filter_size):
        print ("initializing lenet class")
        # network config options
        self.n_filters = n_filters
        self.filter_size = filter_size 
        # params
        self.batch_size = 32
        self.num_classes = 10
        self.epochs = 200
        self.num_predictions = 20
        self.model_dir = os.path.join(os.getcwd(), 'trained_models')
        self.model_name = "lenet-cifar10.h5"
        if dataset == "cifar10":
            from keras.datasets import cifar10
            (self.x_train, self.y_train), (self.x_test, self.y_test) = cifar10.load_data()
            # Convert class vectors to binary class matrices.
            self.y_train = keras.utils.to_categorical(self.y_train, 
                                                      self.num_classes)
            self.y_test = keras.utils.to_categorical(self.y_test, 
                                                     self.num_classes)

        self.train_model()
    
    def train_model(self):
        """This function is used for model architecture
        """
        model = Sequential()
        model.add(Conv2D(
                        self.n_filters, 
                        (self.filter_size, self.filter_size), 
                        padding='same',
                        input_shape=self.x_train.shape[1:])
                        )
        model.add(Activation('relu'))
        
        model.add(Conv2D(
                        self.n_filters, 
                        (self.filter_size, self.filter_size))
                        )
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(
                        2*self.n_filters, 
                        (self.filter_size, self.filter_size), 
                        padding='same')
                        )
        model.add(Activation('relu'))

        model.add(Conv2D(
                        self.n_filters, 
                        (self.filter_size, self.filter_size))
                        )
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(512))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.num_classes))
        model.add(Activation('softmax'))
        # initiate RMSprop optimizer
        opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)
        model.compile(loss='categorical_crossentropy',
                      optimizer=opt,
                      metrics=['accuracy'])
        self.x_train = self.x_train.astype('float32')
        self.x_test = self.x_test.astype('float32')
        self.x_train /= 255
        self.x_test /= 255

        # fit the model 
        model.fit(self.x_train, 
                  self.y_train,
                  batch_size=self.batch_size,
                  epochs=self.epochs,
                  validation_data=(self.x_test, self.y_test),
                  shuffle=True)
        
        if not os.path.isdir(save_dir):
            os.makedirs(self.model_dir)
            self.model_path = os.path.join(self.model_dir, self.model_name)
            model.save(self.model_path)
            print ("model saved")





        
if __name__=="__main__":
    Lenet("cifar10", 32, 3)

"""
# Score trained model.
scores = model.evaluate(x_test, y_test, verbose=1)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])
"""
=======
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ResNet50 v1.0
# Paper: https://arxiv.org/pdf/1512.03385.pdf

import tensorflow as tf
from tensorflow.keras import Model
import tensorflow.keras.layers as layers

def stem(inputs):
    """ Create the Stem Convolutional Group 
        inputs : the input vector
    """
    # The 224x224 images are zero padded (black - no signal) to be 230x230 images prior to the first convolution
    x = layers.ZeroPadding2D(padding=(3, 3))(inputs)
    
    # First Convolutional layer which uses a large (coarse) filter 
    x = layers.Conv2D(64, kernel_size=(7, 7), strides=(2, 2), padding='valid', use_bias=False, kernel_initializer='he_normal')(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    
    # Pooled feature maps will be reduced by 75%
    x = layers.ZeroPadding2D(padding=(1, 1))(x)
    x = layers.MaxPool2D(pool_size=(3, 3), strides=(2, 2))(x)
    return x

def bottleneck_block(n_filters, x):
    """ Create a Bottleneck Residual Block with Identity Link
        n_filters: number of filters
        x        : input into the block
    """
    # Save input vector (feature maps) for the identity link
    shortcut = x
    
    ## Construct the 1x1, 3x3, 1x1 residual block (fig 3c)

    # Dimensionality reduction
    x = layers.Conv2D(n_filters, (1, 1), strides=(1, 1), use_bias=False, kernel_initializer='he_normal')(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)

    # Bottleneck layer
    x = layers.Conv2D(n_filters, (3, 3), strides=(1, 1), padding="same", use_bias=False, kernel_initializer='he_normal')(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)

    # Dimensionality restoration - increase the number of output filters by 4X
    x = layers.Conv2D(n_filters * 4, (1, 1), strides=(1, 1), use_bias=False, kernel_initializer='he_normal')(x)
    x = layers.BatchNormalization()(x)

    # Add the identity link (input) to the output of the residual block
    x = layers.add([shortcut, x])
    x = layers.ReLU()(x)
    return x

def projection_block(n_filters, x, strides=(2,2)):
    """ Create Bottleneck Residual Block with Projection Shortcut
        Increase the number of filters by 4X
        n_filters: number of filters
        x        : input into the block
        strides  : whether entry convolution is strided (i.e., (2, 2) vs (1, 1))
    """
    # Construct the projection shortcut
    # Increase filters by 4X to match shape when added to output of block
    shortcut = layers.Conv2D(4 * n_filters, (1, 1), strides=strides, use_bias=False, kernel_initializer='he_normal')(x)
    shortcut = layers.BatchNormalization()(shortcut)

    ## Construct the 1x1, 3x3, 1x1 residual block (fig 3c)

    # Dimensionality reduction
    # Feature pooling when strides=(2, 2)
    x = layers.Conv2D(n_filters, (1, 1), strides=strides, use_bias=False, kernel_initializer='he_normal')(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)

    # Bottleneck layer
    x = layers.Conv2D(n_filters, (3, 3), strides=(1, 1), padding='same', use_bias=False, kernel_initializer='he_normal')(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)

    # Dimensionality restoration - increase the number of filters by 4X
    x = layers.Conv2D(4 * n_filters, (1, 1), strides=(1, 1), use_bias=False, kernel_initializer='he_normal')(x)
    x = layers.BatchNormalization()(x)

    # Add the projection shortcut link to the output of the residual block
    x = layers.add([x, shortcut])
    x = layers.ReLU()(x)
    return x

def classifier(x, n_classes):
  """ Create the Classifier Group 
      x         : input to the classifier
      n_classes : number of output classes
  """
  # Pool at the end of all the convolutional residual blocks
  x = layers.GlobalAveragePooling2D()(x)

  # Final Dense Outputting Layer for the outputs
  outputs = layers.Dense(n_classes, activation='softmax')(x)
  return outputs


# The input tensor
inputs = layers.Input(shape=(224, 224, 3))

# The stem convolutional group
x = stem(inputs)

# First Residual Block Group of 64 filters
# Double the size of filters to fit the first Residual Group
x = projection_block(64, x, strides=(1,1))

# Identity residual blocks
for _ in range(2):
    x = bottleneck_block(64, x)

# Second Residual Block Group of 128 filters
# Double the size of filters and reduce feature maps by 75% (strides=2, 2) to fit the next Residual Group
x = projection_block(128, x)

# Identity residual blocks
for _ in range(3):
    x = bottleneck_block(128, x)

# Third Residual Block Group of 256 filters
# Double the size of filters and reduce feature maps by 75% (strides=2, 2) to fit the next Residual Group
x = projection_block(256, x)

# Identity residual blocks
for _ in range(5):
    x = bottleneck_block(256, x)

# Fourth Residual Block Group of 512 filters
# Double the size of filters and reduce feature maps by 75% (strides=2, 2) to fit the next Residual Group
x = projection_block(512, x)

# Identity residual blocks
for _ in range(2):
    x = bottleneck_block(512, x)

# The classifier for 1000 classes
outputs = classifier(x, 1000)

# Instantiate the Model
model = Model(inputs, outputs)
>>>>>>> 456bf9ca72b2688b8e0b49686e8b27d164b99367
