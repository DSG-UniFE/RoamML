import random
import time
from tcp_node import TcpNode  # Importing TcpNode class from a module
import sys

node_id = sys.argv[1]  # Get the node ID from command-line arguments

# Create a TcpNode instance and assign an ID from the command-line argument
node = TcpNode(node_id,
               model_path="./models/model.json",
               weight_path="./models/model.h5",
               dataset_path=f"./datasets/cifar10/CIFAR10_subset_{node_id}.npz",
               properties_path=f"./json_nodes/node_{node_id}.json",
               data_gravity_request_timeout=2)

# Let's wait all the warning of tensorflow
time.sleep(5)

# Compute and set the data gravity for the node (mocked with a random value)
node.compute_data_gravity()

# Start the UDP listener thread to respond to data gravity requests
node.respond_data_gravity()

# Start receiving data from satellites
node.receive_satellite()

if node_id == "0":

    # Wait for a second for other nodes to get ready
    time.sleep(5)

    # Request other nodes for IP addresses and Data Gravity
    nodes_gravities = node.request_data_gravity()

    # Orders the nodes_gravities list, with data gravity value as the key, in descending order
    #nodes_gravities.sort(key=lambda x: x[2], reverse=True)

    from support_functions import sort_nodes_gravities
    nodes_gravities = sort_nodes_gravities(nodes_gravities)

    jobs = ['update', 'train', 'send']
    sat = node.create_satellite(satellite_id="0", trip=nodes_gravities, jobs=jobs)


    # Append the created satellite to the node's satellite list
    node.append_satellite(sat)

    # Node zero will execute satellite loading model
    node.execute_satellites(load_model_from_file=True)


while True:
    if node_id == "0":
        node.execute_satellites()
        node.check_completed_satellites()
    else:
        node.execute_satellites(shutdown_node=True)
    time.sleep(15)
