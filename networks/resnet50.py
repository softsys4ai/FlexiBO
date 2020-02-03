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

import os 
import tensorflow as tf
from tensorflow.keras import Model
import tensorflow.keras.layers as layers

def stem(inputs, n_filters):
    """ Create the Stem Convolutional Group 
        inputs : the input vector
    """
    # The 224x224 images are zero padded (black - no signal) to be 230x230 images prior to the first convolution
    x = layers.ZeroPadding2D(padding=(3, 3))(inputs)
    
    # First Convolutional layer which uses a large (coarse) filter 
    x = layers.Conv2D(n_filters, kernel_size=(7, 7), strides=(2, 2), padding='valid', use_bias=False, kernel_initializer='he_normal')(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    
    # Pooled feature maps will be reduced by 75%
    x = layers.ZeroPadding2D(padding=(1, 1))(x)
    x = layers.MaxPool2D(pool_size=(3, 3), strides=(2, 2))(x)
    return x

def bottleneck_block(n_filters, filter_size, x):
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
    x = layers.Conv2D(n_filters, (filter_size, filter_size), strides=(1, 1), padding="same", use_bias=False, kernel_initializer='he_normal')(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)

    # Dimensionality restoration - increase the number of output filters by 4X
    x = layers.Conv2D(n_filters * 4, (1, 1), strides=(1, 1), use_bias=False, kernel_initializer='he_normal')(x)
    x = layers.BatchNormalization()(x)

    # Add the identity link (input) to the output of the residual block
    x = layers.add([shortcut, x])
    x = layers.ReLU()(x)
    return x

def projection_block(n_filters, filter_size, x, strides=(2,2)):
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
    x = layers.Conv2D(n_filters, (filter_size, filter_size), strides=(1, 1), padding='same', use_bias=False, kernel_initializer='he_normal')(x)
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
    projection_block_n_filters,
    projection_block_filter_size,
    bottleneck_block_n_filters,
    bottleneck_block_filter_size,)=get_configurable_hyperparams()
    
    # The input tensor
    inputs = layers.Input(shape=(224, 224, 3))

    # The stem convolutional group
    x = stem(inputs, stem_n_filters)
    # First Residual Block Group of 64 filters
    # Double the size of filters to fit the first Residual Group
    x = projection_block(projection_block_n_filters,projection_block_filter_size, x, 
                     strides=(1,1))
    # Identity residual blocks
    for _ in range(2):
        x = bottleneck_block(bottleneck_block_n_filters,projection_block_filter_size, x)
    # Second Residual Block Group of 128 filters
    # Double the size of filters and reduce feature maps by 75% (strides=2, 2) to fit the next Residual Group
    x = projection_block(2*projection_block_n_filters,projection_block_filter_size, x)
    # Identity residual blocks
    for _ in range(3):
        x = bottleneck_block(2*bottleneck_block_n_filters,bottleneck_block_filter_size, x)
    # Third Residual Block Group of 256 filters
    # Double the size of filters and reduce feature maps by 75% (strides=2, 2) to fit the next Residual Group
    x = projection_block(4*projection_block_n_filters,projection_block_filter_size, x)
    # Identity residual blocks
    for _ in range(5):
        x = bottleneck_block(4*bottleneck_block_n_filters,bottleneck_block_filter_size, x)
    # Fourth Residual Block Group of 512 filters
    # Double the size of filters and reduce feature maps by 75% (strides=2, 2) to fit the next Residual Group
    x = projection_block(8*projection_block_n_filters,projection_block_filter_size, x, x)
    # Identity residual blocks
    for _ in range(2):
        x = bottleneck_block(8*bottleneck_block_n_filters,bottleneck_block_filter_size, x)

    # The classifier for 1000 classes
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