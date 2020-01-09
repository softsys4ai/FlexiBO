
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


