

#NN packages
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.utils import plot_model
import numpy as np

class SkyNet:#args = inputs
    #In Keras, the input layer itself is NOT a layer, but a tensor.
    #It's the starting tensor you send to the first hidden layer.
    #This tensor must have the same 'shape' as the training data.
    def __init__(self):
        self.input1 = -1
        self.input2 = -1
        self.input3 = -1
        self.input4 = -1
        #since we only have 4 inputs, the tensor for input will look like (named tensor I): {Ia,Ib,Ic,Id}
        self.inpTensor = np.atleast_2d(np.asarray([self.input1, self.input2, self.input3, self.input4]))
                         #Tensor I = ( Ia   ,   Ib  ,   Ic  ,   Id  )
        self.model = Sequential()

        #start from the first hidden layer, since the input is not actually a layer...
        #...but inform the shape (shape=how many) of the input, with 4 elements.
        #comma neccesary when your inputs are 1 dimensional, because 'input_shape' takes in a Tuple
        #
        #create layer which will: take in 4 inputs, pass them through an activation function, then give it to this layer:
        hiddenLayer1 = Dense(units = 5, activation = 'relu',input_shape = (4,) )#1st hidden layer of 5 nodes
        #
        hiddenLayer2 = Dense(units=5, activation = 'relu')#2nd hidden layer of 5 nodes.
        outputLayer = Dense(units=1, activation = 'sigmoid')#layer that contains the output. (number 0.0 to 1.0)

        #adds hidden layers to model sequentially
        self.model.add(hiddenLayer1)
        self.model.add(hiddenLayer2)
        self.model.add(outputLayer)
        #layers will look like: 4 -> 5 -> 5 -> 1
    
        self.model.compile(loss='mse', optimizer='adam',metrics=['accuracy'])

        plot_model(self.model,show_shapes=True, show_layer_names=True, to_file='NN_model.png')#creates a graphic visualization of the network
        print('created SkyNet . . .')
