import numpy as np

# Define the function to calculate Shannon's entropy

def shannon_entropy_calulation(dataset_path, encoder=None):

    try:
        data = np.load(dataset_path, allow_pickle=True)
    except:
        return None
    
    labels = data['array2']#data['data'][1]

    # inverse encode
    # labels = encoder.inverse_transform(labels)

    # Get the unique labels and their counts
    unique_labels, label_counts = np.unique(labels, return_counts=True)

    num_classes = len(unique_labels)

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
        return entropy / np.log2(num_classes)


def sort_nodes_gravities(nodes_gravities, criterion_types=None, method='BWM', mic=None, lic=None):

    import numpy as np
    from pyDecision.algorithm import entropy_method
    from pyDecision.algorithm import bw_method
    from pyDecision.algorithm import topsis_method

    if not mic:
        mic = np.array([3, 1, 3, 4, 4, 6, 7, 9])

    if not lic:
        # LIC: Ranking of criteria based on their least importance.
        # Example: Criterion 6 (index 5) is identified as the least important.
        lic = np.array([7, 9, 3, 4, 4, 3, 3, 1])

    if not criterion_types:
        # Array of criterion types, indicating optimization direction for each criterion.
        # 'max' implies the criterion should be maximized, while 'min' implies minimization.
        # This example assumes all but the last criterion are to be maximized.
        criterion_types = np.array(['max', 'max', 'max', 'max', 'max', 'max', 'max', 'min'])

    

    for ng in nodes_gravities:
        print(ng)
        
    
    if len(nodes_gravities) <= 1:
        return nodes_gravities

    # RoamML data gravity format:
    #('address','node_id',{'Data volume': 81914398, 'Data distribution': 0.9550629211855005, 'CPU power': 5200, 'GPU power': 2000, 'Total Ram': 10, 'Battery Capacity': 3500, 'Bandwidth': 110, 'Latency': 6})

    # This function logic: 
    #{'node_id': [4096, 0.5, 1200, 2800, 6, 1500, 70, 5]}

    # Create matrix of normalized criteria values (rows: nodes, columns: criteria)

    # Rows = the number of nodes, Columns = the number of properties
    # ---> ALL THE NODES MUST HAVE THE SAME NUMBER OF PROPERTIES <---
    matrix = np.zeros((len(nodes_gravities), len(list(nodes_gravities[0][2].values()))))

    for i, node in enumerate(nodes_gravities):
        #matrix[i] = np.array(list(nodes_gravities[i].values())[0])
        matrix[i] = np.array(list(nodes_gravities[i][2].values()))

    matrix = np.round(matrix, decimals=3)


    if method == 'Single':
        print('Sorting node with Single Method')
        # Initialize weights to zero
        weights = np.zeros(len(list(nodes_gravities[0][2].values())))
        # Set the weight of the first criterion (assuming criterion index to sort by is the first)
        # First Criteria is is the size of the dataset
        weights[0] = 1

    if method == 'Entropy':
      # Entropy weight calculation
      print('Sorting node with Entropy weights')
      weights = entropy_method(matrix, criterion_types)

    if method == 'BWM' :
      print('Sorting node with Best worst weights')
      # Call BWM Function
      weights = bw_method(mic, lic, eps_penalty = 1, verbose = True)

    # if method == 'Entropy':
    #     # Entropy weight calculation
    #     print('Entropy weights')
    #     weights = entropy_method(matrix, criterion_types)
    # else:
    #     print('Best worst weights')
    #     # Call BWM Function
    #     weights = bw_method(mic, lic, eps_penalty = 1, verbose = True)

    # Use TOPSIS to create rank
    rank = topsis_method(matrix, weights, criterion_types, graph = False, verbose =False)

    # Get sorted indices based on TOPSIS ranks
    sorted_indices = np.argsort(-rank)

    # Reorder nodes based on sorted indices
    sorted_nodes = [nodes_gravities[i] for i in sorted_indices]

    return sorted_nodes