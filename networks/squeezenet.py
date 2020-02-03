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

# SqueezeNet v1.0 (2016)
# Paper: https://arxiv.org/pdf/1602.07360.pdf

import os 
import tensorflow as tf
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Concatenate, Dropout
from tensorflow.keras.layers import GlobalAveragePooling2D, Activation

def stem(inputs, n_filters, filter_size):
    ''' Construct the Stem Group  
	inputs: the input tensor
    '''
    x = Conv2D(n_filters, (filter_size, filter_size), strides=2, 
               padding='same', activation='relu', kernel_initializer='glorot_uniform')(inputs)
    x = MaxPooling2D(3, strides=2)(x)
    return x

def learner(x, fire_group1_n_filters, fire_group2_n_filters,
            fire_block_n_filters):
    ''' Construct the Learner
   	x    : input to the learner
    '''
    # First fire group, progressively increase number of filters
    x = group(x, [fire_group1_n_filters, fire_group1_n_filters, 2*fire_group1_n_filters])

    # Second fire group
    x = group(x, [fire_group2_n_filters, 1.5*fire_group2_n_filters, 1.5*fire_group2_n_filters, 2*fire_group2_n_filters])

    # Last fire block (module)
    x = fire_block(x, fire_block_n_filters)

    # Dropout is delayed to end of fire groups
    x = Dropout(0.5)(x)
    return x

def group(x, filters):
    ''' Construct a Fire Group
        x     : input to the group
        filters: list of number of filters per fire block (module)
    '''
    # Add the fire blocks (modules) for this group
    for n_filters in filters:
        x = fire_block(x, n_filters)

    # Delayed downsampling
    x = MaxPooling2D((3, 3), strides=(2, 2))(x)
    return x


def fire_block(x, n_filters):
    ''' Construct a Fire Block
	x        : input to the block
        n_filters: number of filters
    '''
    # squeeze layer
    squeeze = Conv2D(n_filters, (1, 1), strides=1, activation='relu',
                     padding='same', kernel_initializer='glorot_uniform')(x)

    # branch the squeeze layer into a 1x1 and 3x3 convolution and double the number
    # of filters
    expand1x1 = Conv2D(n_filters * 4, (1, 1), strides=1, activation='relu',
                      padding='same', kernel_initializer='glorot_uniform')(squeeze)
    expand3x3 = Conv2D(n_filters * 4, (3, 3), strides=1, activation='relu',
                      padding='same', kernel_initializer='glorot_uniform')(squeeze)

    # concatenate the feature maps from the 1x1 and 3x3 branches
    x = Concatenate()([expand1x1, expand3x3])
    return x

def classifier(x, n_classes):
    ''' Construct the Classifier 
	x        : input to the classifier
	n_classes: number of output classes
    '''
    # set the number of filters equal to number of classes
    x = Conv2D(n_classes, (1, 1), strides=1, activation='relu', 
               padding='same', kernel_initializer='glorot_uniform')(x)

    # reduce each filter (class) to a single value
    x = GlobalAveragePooling2D()(x)
    x = Activation('softmax')(x)
    return x

def get_configurable_hyperparams():
    """This function is used to ge the configurable hyperparameters 
    """
    import yaml
    with open("cur_config.yaml") as fp:
            cur_cfg=yaml.load(fp)
    return (cur_cfg["cur_conf"][0], cur_cfg["cur_conf"][1], cur_cfg["cur_conf"][2],
            cur_cfg["cur_conf"][3], cur_cfg["cur_conf"][4])

def get_data():
    """This function is used to get train and test data
    """
    from tensorflow.keras.datasets import cifar10 
    import numpy as np
    (x_train, y_train), (x_test, y_test) = cifar10.load_data() 
    x_train = (x_train / 255.0).astype(np.float32) 
    x_test = (x_test / 255.0).astype(np.float32) 
    return x_train, y_train, x_test, y_test

if __name__=="__main__":
    
    # get configurable hyperparams
    (stem_n_filters,
    stem_filter_size,
    fire_group1_n_filters,
    fire_group2_n_filters,
    fire_block_n_filters)=get_configurable_hyperparams()
    # The input shape
    inputs = Input((224, 224, 3))
    # The Stem Group
    x = stem(inputs, stem_n_filters, stem_filter_size)
    # The Learner
    x = learner(x, fire_group1_n_filters, fire_group2_n_filters, 
                fire_block_n_filters)
    # The classifier
    outputs = classifier(x, 1000)

    # Instantiate the Model
    model = Model(inputs, outputs)
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['acc'])
    model.summary()

    xtrain, ytrain, x_test, y_test=get_data()    
    # train model
    model.fit(x_train, y_train, epochs=10, 
              batch_size=32, validation_split=0.1, verbose=1)
    
    # save model
    fmodel=os.path.join(os.getcwd(),"model.h5") 
    model.save(fmodel)

