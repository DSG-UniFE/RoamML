import numpy as np
from tensorflow.keras.models import Sequential, model_from_json
from keras.utils import to_categorical


# form sklearn.metrics import f1_score

class Satellite:

    def __init__(self, satellite_id, trip, jobs, creator_node_id):
        """
        Initialize a Satellite object with the provided parameters.

        Args:
            satellite_id (str): The unique identifier for the satellite.
            trip (list): List of Tuples representing the trip plan for the satellite. Each Tuple consist in
                            (node_address, node_id, data_gravity).
            jobs (list): The list of jobs to be performed by the satellite.
            creator_node_id (str): The identifier of the node that created the satellite.
        """

        self.trip = []

        # prepare the trip as the original tuple with another element representing the state of the node in the map:
        #   -1  =   Unvisited node
        #   0   =   Actual node
        #   +1  =   Visited node

        for i, el in enumerate(trip):
            if i == 0:
                self.trip.append((el[0], el[1], el[2], 0))
            else:
                self.trip.append((el[0], el[1], el[2], -1))

        self.model = None
        self.creator_id = creator_node_id
        # self.trip = trip
        self.id = satellite_id
        self.jobs = jobs
        self.actual_node = 0
        self.dataset = None
        self.train_completed = False

    def update_trip(self, new_trip):
        """
        Updates the satellite trip with the unseen nodes in the new trip.

        Returns:
            None
        """

        info = " *** Update Trip *** \n"

        info += f"self.trip before new nodes sorting:\n"
        info += f"{self.get_destinations_info()}\n"

        for new_node in new_trip:
            if new_node[0] not in map(lambda x: x[0], self.trip):
                self.trip.append((new_node[0], new_node[1], new_node[2], -1))
                info += f"'{new_node[0]}' appended in trip\n"
            else:
                info += f"'{new_node[0]}' *** NOT *** appended in trip\n"

        info += f"self.trip pre sorting:\n"
        info += f"{self.get_destinations_info()}\n"

        # Put apart all the unvisited nodes (old and new) from the actual one and the visited
        unseen_trip = []
        for node in self.trip:
            if node[3] == -1:
                unseen_trip.append(node)
                self.trip.remove(node)
        # Re-order the unseen_trip
        unseen_trip.sort(key=lambda x: x[2], reverse=True)

        # Merge the trip with the sorted unseen list of nodes
        self.trip += unseen_trip

        info += f"self.trip post sorting:\n"
        info += f"{self.get_destinations_info()}\n"

        info += " *** End Update Trip ***"

        return info

    def load_model(self, model_path, weight_path):
        """
        Load a neural network model from disk and set it as the satellite's model.

        Returns:
            str: A message indicating that the model was loaded from disk.
        """
        # load json and create model
        json_file = open(model_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(weight_path)
        self.model = loaded_model

        return "Loaded model from disk"

    def train_model(self):
        """
        Train the loaded neural network model using the satellite's dataset.

        This method assumes that the dataset and model are already loaded.

        Returns:
            None
        """
        x_train = np.expand_dims(self.dataset['data'][0], axis=-1)
        y_train = to_categorical(self.dataset['data'][1], num_classes=10)
        current_epochs = 10
        # epochs_list.append(current_epochs)
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        history_x = self.model.fit(x_train, y_train, epochs=current_epochs, batch_size=64, validation_split=0.2,
                                   verbose=2)

    def get_model_performance(self):

        testset_x = np.load('datasets/mnist-roamml/MNIST_test_images.npz',
                            mmap_mode='r',
                            allow_pickle=True)

        testset_y = np.load('datasets/mnist-roamml/MNIST_test_labels.npz',
                            mmap_mode='r',
                            allow_pickle=True)

        x_test = np.expand_dims(testset_x['arr_0'], axis=-1)
        y_test = to_categorical(testset_y['arr_0'], num_classes=10)

        loss, acc = self.model.evaluate(x_test, y_test, verbose=0)

        from sklearn.metrics import f1_score, roc_auc_score
        from sklearn.preprocessing import LabelBinarizer

        predictions = self.model.predict(x_test)

        # Convert predictions to class labels
        predicted_labels = np.argmax(predictions, axis=1)

        original_labels = np.argmax(y_test, axis=1)

        # Calculate F1 Score
        f1 = f1_score(original_labels, predicted_labels, average='weighted')

        lb = LabelBinarizer()
        y_test_one_hot = lb.fit_transform(original_labels)

        roc_score = roc_auc_score(y_test_one_hot, predictions, multi_class='ovr')

        return loss, acc, f1, roc_score

    def debug(self):
        """
        Print debugging information about the satellite's trip, ID, and jobs.

        This method is for debugging purposes.

        Returns:
            None
        """
        print(self.trip, self.id, self.jobs)

    def get_jobs(self):
        """
        Get the list of jobs to be performed by the satellite.

        Returns:
            list: List of jobs.
        """
        return self.jobs

    def get_trip(self):
        """
        Get the trip plan of the satellite.

        Returns:
            list: List representing the trip plan.
        """
        return self.trip

    def get_next_destination(self):
        """
        Get the next destination node from the satellite's trip plan.

        Returns:
            str: The next destination node's identifier.
        """

        i = 0
        for el in self.trip:
            if el[3] == 0:  # Actual node
                break
            i += 1

        try:
            return self.trip[i + 1][0]
        except Exception:
            return None

        # try:
        #     return self.trip[self.actual_node + 1][0]
        # except Exception:
        #     return None

    def get_home_destination(self):
        """
        Get the home destination node from the satellite's trip plan.

        Returns:
            str: The home destination node's identifier.
        """
        return self.trip[0][0]

    def load_dataset(self, path='./datasets/dataset.npz'):
        """
        Load the dataset from a given path.

        Returns:
            tuple: A tuple representing the shape of the loaded dataset.
        """
        self.dataset = np.load(path,
                               mmap_mode='r',
                               allow_pickle=True)
        return self.dataset['data'].shape

    def unload_dataset(self):
        """
        Unload the loaded dataset from the satellite.

        Returns:
            None
        """
        self.dataset = None

    def set_new_actual_node(self):
        """
        Set the next node in the trip plan as the new actual node.

        This is used to track the satellite's progress in the trip plan.

        Returns:
            None
        """
        self.actual_node += 1

        i = 0
        for el in self.trip:
            if el[3] == 0:  # Actual node
                self.trip.remove(el)
                self.trip.insert(i, (el[0], el[1], el[2], +1))
            elif el[3] == -1:  # Unvisited node
                self.trip.remove(el)
                self.trip.insert(i, (el[0], el[1], el[2], 0))
                break
            i += 1

    def set_train_completed(self):
        """
        Set the flag for the completion of the training.

        This is used to avoid the satellite's re-execution when it comes back to the first node.

        Returns:
            None
        """
        self.train_completed = True

    def is_train_completed(self):
        """
        Returns the completion status of the training.

        This is used to avoid the satellite's re-execution when it comes back to the first node.

        Returns:
            Bool: The actual completion status of the satellite
        """
        return self.train_completed

    def get_destinations_info(self):
        """
        Get a string of all destinations in the satellite's trip plan, each destination in a line, and the total
        amount of hops.

        Returns:
            String: info destinations in the trip plan.
        """
        destinations = "\n"
        for el in self.trip:
            destinations += f"{el}\n"
        destinations += f"Total hops: {len(self.trip)}"
        return destinations
