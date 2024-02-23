import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical
import numpy as np

class LSTMNet:
    def __init__(self, n_features, lstm_units=50, output_units=1, output_activation='linear'):
        """
        Initializes the LSTMNet model.
        :param n_features: Number of features in the input data.
        :param lstm_units: Number of units in the LSTM layer.
        :param output_units: Number of units in the output layer.
        :param output_activation: Activation function for the output layer.
        """
        self.n_features = n_features
        self.lstm_units = lstm_units
        self.output_units = output_units
        self.output_activation = output_activation
        self.model = self.build_model()

    def build_model(self):
        """
        Builds the LSTM model.
        """
        model = Sequential([
            LSTM(self.lstm_units, input_shape=(1, self.n_features)),
            Dense(self.output_units, activation=self.output_activation)
        ])
        return model

    def compile(self, optimizer='adam', loss='mean_squared_error', metrics=['accuracy']):
        """
        Compiles the LSTM model.
        :param optimizer: Optimizer to use.
        :param loss: Loss function.
        :param metrics: List of metrics to evaluate during training/testing.
        """
        self.model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    def train(self, X_train, y_train, epochs=10, batch_size=32, validation_data=None):
        """
        Trains the LSTM model.
        :param X_train: Training data.
        :param y_train: Training labels.
        :param epochs: Number of epochs to train for.
        :param batch_size: Batch size for training.
        :param validation_data: Optional validation data.
        """
        X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))  # Reshaping for LSTM
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=validation_data)

    def evaluate(self, X_test, y_test):
        """
        Evaluates the model on the test set.
        :param X_test: Test data.
        :param y_test: Test labels.
        """
        X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))  # Reshaping for LSTM
        return self.model.evaluate(X_test, y_test)

    def predict(self, X):
        """
        Makes predictions with the model.
        :param X: Input data for prediction.
        """
        X = X.reshape((X.shape[0], 1, X.shape[1]))  # Reshaping for LSTM
        return self.model.predict(X)


def main():
    n_features = 10  # For a 1x10 input vector
    model = LSTMNet(n_features=n_features, lstm_units=50, output_units=2, output_activation='softmax')
    # activation and loss functions will need to be adjusted for a regression problem
    # for a one-hot encoded output, output_units must equal n_classes
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    n_sequences = 1000  # Number of sequences
    n_features = 10  # Number of features in each sequence
    n_classes = 2  # Number of output classes (binary classification)

    # Generate random sequences
    x = np.random.rand(n_sequences, n_features)  # Shape: (1000, 10)

    y = np.random.randint(n_classes, size=(n_sequences, 1))  # Shape: (1000, 1)
    y_enc = to_categorical(y, num_classes=n_classes)  # One-hot encoding of labels

    model.train(x, y_enc, epochs=10, batch_size=32)


if __name__ == '__main__':
    main()