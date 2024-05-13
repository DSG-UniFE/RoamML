import numpy as np
from tensorflow.keras.models import Sequential, model_from_json
from keras.utils import to_categorical

import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical
from keras.optimizers import Adam

from tensorflow.keras.models import Sequential

from sklearn.utils import class_weight
from keras import backend as K



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
        self.testset = None
        self.train_completed = False

        self.memory_buffer = []
        self.memory_buffer_size = 250

        self.lr = 0.001
        self.decay_lr = 0.7

        self.training_epochs = 1
        self.replay_epochs = 1

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
        #unseen_trip.sort(key=lambda x: x[2], reverse=True)
        from support_functions import sort_nodes_gravities
        unseen_trip = sort_nodes_gravities(unseen_trip)

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
        subset_data, subset_labels = self.dataset['array1'], self.dataset['array2']
        test_images, test_labels = self.testset['array1'], self.testset['array2']

        # epochs_list.append(current_epochs)
        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        history_x = self.model.fit(subset_data, subset_labels,
                              epochs=self.training_epochs,
                              # class_weight=class_weights,
                              validation_data=(test_images, test_labels))

    def get_model_performance(self):

        # testset_x = np.load('datasets/cifar10/subset_testset.npz',
        #                     mmap_mode='r',
        #                     allow_pickle=True)

        # testset_y = np.load('datasets/mnist-roamml/MNIST_test_labels.npz',
        #                     mmap_mode='r',
        #                     allow_pickle=True)

        # x_test = np.expand_dims(testset_x['arr_0'], axis=-1)
        # y_test = to_categorical(testset_y['arr_0'], num_classes=10)

        # loss, acc = self.model.evaluate(x_test, y_test, verbose=0)

        # from sklearn.metrics import f1_score, roc_auc_score
        # from sklearn.preprocessing import LabelBinarizer

        # predictions = self.model.predict(x_test)

        # # Convert predictions to class labels
        # predicted_labels = np.argmax(predictions, axis=1)

        # original_labels = np.argmax(y_test, axis=1)

        # # Calculate F1 Score
        # f1 = f1_score(original_labels, predicted_labels, average='weighted')

        # lb = LabelBinarizer()
        # y_test_one_hot = lb.fit_transform(original_labels)

        # roc_score = roc_auc_score(y_test_one_hot, predictions, multi_class='ovr')

                # test the model on the test set
        test_images, test_labels = self.testset['array1'], self.testset['array2']
        loss, acc, *is_anything_else_being_returned = self.model.evaluate(test_images, test_labels)
        print('Test accuracy:', acc)

        # test the model on the test set calculate the f1 score
        from sklearn.metrics import f1_score
        y_pred = self.model.predict(test_images)
        y_pred = np.argmax(y_pred, axis=1)
        f1 = f1_score(test_labels, y_pred, average='macro')

        roc_score = 0

        # print the confusion matrix
        # from sklearn.metrics import confusion_matrix
        # print("confusion_matrix:\n", confusion_matrix(test_labels, y_pred))

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
        return self.dataset['array1'].shape
    
    def load_testset(self, path='datasets/cifar10/CIFAR10_subset_testset.npz'):
        """
        Load the testset from a given path.

        Returns:
            tuple: A tuple representing the shape of the loaded testset.
        """
        self.testset = np.load(path,
                    mmap_mode='r',
                    allow_pickle=True)
        return self.testset['array1'].shape

    def unload_dataset(self):
        """
        Unload the loaded dataset from the satellite.

        Returns:
            None
        """
        self.dataset = None

    def unload_testset(self):
        """
        Unload the loaded testset from the satellite.

        Returns:
            None
        """
        self.testset = None

        # Function to add data to memory buffer with random replacement
    def add_to_memory_buffer(self, data, labels, replacement_ratio=0.5):

        # Make copies of the data and labels to avoid modifying the original arrays
        data = np.copy(data)
        labels = np.copy(labels)

        # Check if the memory buffer is not full
        if len(self.memory_buffer) < self.memory_buffer_size:
            # Calculate the number of elements to add to the memory buffer
            num_to_add = min(len(data), self.memory_buffer_size - len(self.memory_buffer))
            
            # Add the elements to the memory buffer
            for i in range(num_to_add):
                self.memory_buffer.append((np.array(data[i]), np.array(labels[i])))

            # Remove the added elements from the data and labels arrays
            data = data[num_to_add:]
            labels = labels[num_to_add:]

        # Check if the memory buffer is full and there are remaining elements in the data array
        if len(self.memory_buffer) >= self.memory_buffer_size and len(data) > 0:
            # Calculate the number of elements to replace in the memory buffer
            num_to_replace = int(replacement_ratio * self.memory_buffer_size)
            
            # Get the unique labels in the labels array
            unique_labels = np.unique(labels)
            
            # Count the occurrences of each label in the memory buffer
            current_label_counts = np.bincount([int(tup[1]) for tup in self.memory_buffer], minlength=np.max(labels)+1)
            
            # Calculate the desired count of instances per class in the memory buffer
            desired_count_per_class = len(self.memory_buffer) // len(unique_labels)
            
            # Calculate the replacement needs for each class
            replacement_needs = {label: desired_count_per_class - current_label_counts[label] for label in unique_labels}

            # Perform the replacements
            for _ in range(num_to_replace):
                # Prioritize classes with the greatest need for adjustment
                adjustments = sorted(replacement_needs.items(), key=lambda x: x[1], reverse=True)
                for label, need in adjustments:
                    if need > 0:
                        # Need more instances of this class
                        add_indices = [i for i, l in enumerate(labels) if l == label]
                        if not add_indices:
                            continue  # No more instances available to add
                        add_index = np.random.choice(add_indices)
                    else:
                        # Too many instances, look for a class to reduce
                        reduce_label = label
                        reduce_indices = [i for i, (_, l) in enumerate(self.memory_buffer) if l == reduce_label]
                        if not reduce_indices:
                            continue  # No instances left to remove
                        add_index = np.random.choice(reduce_indices)

                    # Execute replacement
                    if need > 0:
                        replace_index = np.random.choice([i for i, (_, l) in enumerate(self.memory_buffer) if l != label])
                        self.memory_buffer[replace_index] = (np.array(data[add_index]), np.array(labels[add_index]))
                        # Update counts and needs
                        current_label_counts[labels[add_index]] += 1
                        current_label_counts[int(self.memory_buffer[replace_index][1])] -= 1
                        replacement_needs[label] -= 1  # Decrease the need for this class
                        # Remove replaced elements from data and labels
                        data = np.delete(data, add_index, axis=0)
                        labels = np.delete(labels, add_index, axis=0)
                    else:
                        # Adjust replacement needs without adding new data, as it's a reduction case
                        replacement_needs[label] += 1  # Decrease the reduction need for this class

        # Trim the memory buffer to the desired size
        self.memory_buffer = self.memory_buffer[:self.memory_buffer_size]

        return self.calculate_entropy_buffer(self.memory_buffer), self.calculate_classes_counts(self.memory_buffer)

    # Function to sample from memory buffer
    def sample_from_memory_buffer(self, batch_size):
        # global memory_buffer

        np.random.seed()

        # If the requested batch size is larger than the buffer size, return all elements in the buffer
        if len(self.memory_buffer) < batch_size:
            sample_data, sample_labels = zip(*self.memory_buffer)
        else:
            # Generate random indices for sampling
            sample_indices = np.random.choice(len(self.memory_buffer), batch_size, replace=False)
            # Use the indices to sample data and labels from the memory buffer
            sample_data, sample_labels = zip(*[self.memory_buffer[idx] for idx in sample_indices])

        return np.array(sample_data), np.array(sample_labels)
    
    def roamml_compute_class_weight(self, class_weight, classes, y):
        """
        Estimates class weights for balancing the dataset. If a class in 'classes' does not appear in 'y',
        a default weight of 1 is assigned.

        :param class_weight: 'balanced' or a dict mapping class labels to weights
        :param classes: array-like of shape (n_classes), list of all the class labels
        :param y: array-like of shape (n_samples), array of class labels for the samples
        :return: array of shape (n_classes,) containing the weights for each class
        """
        from collections import Counter
        import numpy as np

        # Count each class in y
        class_counts = Counter(y)

        if class_weight == 'balanced':
            # Total number of samples
            n_samples = len(y)
            
            # Calculate weight for each class, defaulting to 1 if the class is not in y
            weights = {cls: n_samples / (len(classes) * class_counts.get(cls, 0)) if class_counts.get(cls, 0) != 0 else 1 for cls in classes}
        elif isinstance(class_weight, dict):
            # Use user-defined dictionary if provided, defaulting to 1 if the class is not specified
            weights = {cls: class_weight.get(cls, 1) for cls in classes}
        else:
            raise ValueError("class_weight should be 'balanced' or a dict")

        # Create a list of weights in the order of the classes provided
        class_weights = np.array([weights.get(c, 1.0) for c in classes])

        print(f"c_w: {class_weights}")

        dict_class_weights = dict(zip(classes,class_weights))
        
        print(f"d_c_w: {dict_class_weights}")

        return dict_class_weights


    def experience_replay(self):

        subset_data, subset_labels = self.dataset['array1'], self.dataset['array2']
        test_images, test_labels = self.testset['array1'], self.testset['array2']

        # Update the learning rate and optimizer as necessary
        if self.actual_node in [3, 5, 8]:
            self.lr *= self.decay_lr # CHIEDERE A SIMON


         # Replay experiences from the memory buffer if it's not empty
        if self.memory_buffer:
            
            # read from buffer
            replay_data, replay_labels = self.sample_from_memory_buffer(batch_size=len(subset_data))

            # calculate class weights
            # class_weights = class_weight.compute_class_weight(class_weight = 'balanced',
            #                                         classes = np.unique(replay_labels),
            #                                         y = replay_labels.flatten())

            # class_weights = dict(zip(np.unique(replay_labels),class_weights))

            print(np.array(range(10)))

            class_weights = self.roamml_compute_class_weight(class_weight = 'balanced',
                                                            classes = np.array(range(10)),
                                                            y = replay_labels.flatten())

            # Update the learning rate and optimizer as necessary
            adam = tf.keras.optimizers.Adam(learning_rate=self.lr)

            print(f"replay lr = {self.lr}")
            #self.model.compile(optimizer=adam, loss='sparse_categorical_crossentropy', metrics=['accuracy', f1_m ])
            self.model.compile(optimizer=adam, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
            
            print("\nReplaying from memory buffer\n")
            self.model.fit(replay_data, replay_labels,
                    epochs=self.replay_epochs,
                    class_weight=class_weights,
                    validation_data=(test_images, test_labels))

        # Add the current subset data to the memory buffer
        return self.add_to_memory_buffer(subset_data, subset_labels, replacement_ratio=0.4)

    def shannon_entropy_calculation(self, labels, encoder=None):

        # inverse encode
        # labels = encoder.inverse_transform(labels)

        # Get the unique labels and their counts
        unique_labels, label_counts = np.unique(labels, return_counts=True)

        # Calculate the total number of samples
        total_samples = len(labels)

        # Calculate the probabilities of each label
        probabilities = label_counts / total_samples

        # Calculate the entropy
        entropy = -np.sum(probabilities * np.log2(probabilities))

        # Check if the entropy is 0
        if entropy == 0:
            return 0
        else:
            # Normalize the entropy
            return entropy / np.log2(len(unique_labels))

    def calculate_entropy_buffer(self, memory_buffer):
        all_labels = []
        for i in range(len(memory_buffer)):
            labels = memory_buffer[i][1]
            all_labels.append(labels)
        entropy = self.shannon_entropy_calculation(all_labels)
        return entropy

    def calculate_classes_counts(self, memory_buffer):
        return np.bincount([tup[1] for tup in memory_buffer])

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
