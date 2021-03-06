from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Dense, Activation, Flatten, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

(X_train, y_train), (X_test, y_test) = mnist.load_data()

# reshaping X data: (n, 28, 28) => (n, 28, 28, 1)
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], X_train.shape[2], 1)).astype("float32") / 255.0
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], X_test.shape[2], 1)).astype("float32") / 255.0

# converting y data into categorical (one-hot encoding)
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

print("data ready")

def mnist_model():
    inputs = Input(shape=(28, 28, 1))
    conv = Conv2D(filters=5, kernel_size=(5, 5), strides=(1, 1), padding="same", use_bias=False, name="conv")(inputs)
    batchnorm = BatchNormalization(epsilon=0.001, name="batchnorm")(conv)
    maxpool = MaxPooling2D(pool_size=(2, 2), name="maxpool")(batchnorm)
    relu_maxpool = Activation('relu',name="relu_maxpool")(maxpool)
    flatten = Flatten(name="flatten")(relu_maxpool)
    dense1 = Dense(120, name="dense1")(flatten)
    relu_dense1 = Activation('relu', name="relu_dense1")(dense1)
    dense2 = Dense(10, name="dense2")(relu_dense1)
    outputs = Activation('softmax', name="result")(dense2)
    model = Model(inputs, outputs)

    return model


model = mnist_model()

model.summary()

optimizer = Adam(lr=0.001)

model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

history = model.fit(X_train, y_train, batch_size=100,
                    validation_data=(X_test, y_test), epochs=3, verbose=2)

def save_values(value, name):
    value.tofile(f"value/{name}_tfone.bin")

layer_name_list = ["conv", "batchnorm", "maxpool", "relu_maxpool",
                   "flatten", "dense1", "relu_dense1",
                   "dense2", "result"]

intermediate_output_list = []
for n in layer_name_list:
    intermidiate_layer_model = Model(inputs=model.input, outputs=model.get_layer(n).output)
    intermidiate_output = intermidiate_layer_model.predict(X_test)
    save_values(intermidiate_output, n)
    print(n, ": ", intermidiate_output.shape)

print("=======================================================================")

weights = model.get_weights()

name_list = ["kernel",
             "gamma", "beta",
             "mean", "variance",
             "W1", "b1",
             "W2", "b2"]

def save_weights(weight, name):
    weight.tofile(f"weight/{name}_tfone.bin")

for w, name in zip(weights, name_list):
    save_weights(w, name)
    print(name, ": ", w.shape)

print("Finished!")
