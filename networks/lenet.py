
from __future__ import print_function
import os
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D

class Lenet(object):
    """This class is used to train Lenet
    """
    def __init__(self, n_filters, filter_size):
        print ("initializing lenet class")
        # network config options
        self.n_filters = n_filters
        self.filter_size = filter_size 
        # params
        self.batch_size = 32
        self.num_classes = 10
        self.epochs = 1
        self.num_predictions = 20
        
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
        model.add(Conv2D(self.layer1_n_filters, (self.layer1_filter_size, self.layer1_filter_size), padding='same',
                        input_shape=self.x_train.shape[1:]))
        model.add(Activation('relu'))
        
        model.add(Conv2D(self.layer2_n_filters, (self.layer2_filter_size, self.layer2_filter_size)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(2*self.layer3_n_filters, (self.layer3_filter_size, self.layer3_filter_size), padding='same'))
        model.add(Activation('relu'))

        model.add(Conv2D(self.layer4_n_filters, (self.layer4_filter_size, self.layer4_filter_size)))
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
        model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
        self.x_train = self.x_train.astype('float32')
        self.x_test = self.x_test.astype('float32')
        self.x_train /= 255
        self.x_test /= 255

        # fit the model 
        model.fit(self.x_train, self.y_train, batch_size=self.batch_size,
                  epochs=self.epochs, validation_data=(self.x_test, self.y_test), shuffle=True)
        
         # save model
        fmodel=os.path.join(os.get_cwd(),"model.h5") 
        model.save(fmodel)

def get_configurable_hyperparams():
    """This function is used to ge the configurable hyperparameters 
    """
    import yaml
    with open("cur_config.yaml") as fp:
            cur_cfg=yaml.load(fp)
    return (cur_cfg["cur_conf"][0], cur_cfg["cur_conf"][1], cur_cfg["cur_conf"][2],
            cur_cfg["cur_conf"][3], cur_cfg["cur_conf"][4], cur_cfg["cur_conf"][5],
            cur_cfg["cur_conf"][6], cur_cfg["cur_conf"][7])    

if __name__=="__main__":
    layer1_n_filters, layer1_filter_size, layer2_n_filters, 
    layer2_filter_size, layer3_n_filters, layer3_filter_size, 
    layer4_n_filters, layer3_filter_size)=get_configurable_hyperparams()
    Lenet("cifar10", layer1_n_filters, layer1_filter_size,
         layer2_n_filters, layer2_filter_size, layer3_n_filters, 
         layer3_filter_size, layer4_n_filters, layer4_filter_size)


