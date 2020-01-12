# -----------------------TENSORS:
#Tensors are vectors. The rank of the tensor directly correlates with the dimensions of the vector.
#Example 1: Observe Ray 'A' on a cartesian coordinate plane (x,y,z)
#
#   |     ^
#   |    / A
#  y|   /
#   |  /
#   | /
#   |/___________________________
#               x
#
# Ray A can be expressed by giving it's x and y components.
# (Since it's on a 2D plane, z = 0)
#
#   |     ^
#   |    /A]5
#  y|   /  ]4
#   |  /   ]3
#   | /    ]2
#   |/_____]1_____________________
#    1  2  3        x
#
#   now you can see that Ray 'A' is 3 unit vectors in the x axis
#       and 5 unit vectors in the y axis
#
# Therefore, Ray 'A' = {Ax, Ay, Az}
#                    = {3, 5, 0}
#
#Rank 2:
#
# An example of a Rank 2 Tensor in the real world could be:
#
# Say you have a cube, and you want to do some measurements on force affecting the cube.
#   Now we'll only look at 1 face of the cube (side view):
#   []
#   [] ----> this arrow represents the surfaces direction in respect to the cartesian coordinate system
#   []       therefore this arrow can have the components (x,y,z)
#   []
#   [] ----> this arrow represents the direction of the force affecting this face in respect to the cartesian coordinate system.
#   []      therefore this arrow can also have the components (x,y,z)
#
# This is how the example can be represented.
# the first component represents direction of the face
# the second component represents direction of the force applied to the face.
#       Tensor N = {Nxx,Nxy,Nxz}
#                  {Nyx,Nyy,Nyz}
#                  {Nzx,Nzy,Nzz}
# ---------------------------------------------------------------------------------------------------------------------
#boom. class dismissed.

#NN packages
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.utils import plot_model


def SkyNet(input1, input2, input3, input4, target):#args = inputs
    #In Keras, the input layer itself is NOT a layer, but a tensor.
    #It's the starting tensor you send to the first hidden layer.
    #This tensor must have the same 'shape' as the training data.

    #since we only have 4 inputs, the tensor for input will look like (named tensor I): {Ia,Ib,Ic,Id}
    inpTensor = (input1, input2, input3, input4)
    #Tensor I = ( Ia   ,   Ib  ,   Ic  ,   Id  )

    NN_target = target #target = what the NN should look at to judge success

    model = Sequential()

    #start from the first hidden layer, since the input is not actually a layer
    #but inform the shape of the input, with 4 elements.
    #comma neccesary when your input is 1D, beacuse input_shape takes in a Tuple
    model.add(Dense(units = 5, activation = 'relu',input_shape = (4,) )) #hidden layer 1
    model.add(Dense(units=5)) #hidden layer 2
    model.add(Dense(units=1)) #output layer

    #layers will look like: 4 -> 5 -> 5 -> 1

    #plot_model(model, to_file='NN_model.png')#creates a graphic visualization of the network
    print('done')
