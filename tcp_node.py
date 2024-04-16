import pickle

from node import Node  # Import the Node class from the 'node' module
import threading
import socket
import struct
from satellite import Satellite


class TcpNode(Node):

    def __init__(self, node_id, model_path, weight_path, dataset_path, data_gravity_request_port=50001,
                 data_gravity_request_timeout=30):
        """
        Initialize the TcpNode object.

        Args:
            node_id (str): The unique identifier for the node.
            data_gravity_request_port (int, optional): The port used for data gravity requests (default is 50001).
            data_gravity_request_timeout (int, optional): The timeout in seconds for data gravity requests
            (default is 10).
        """
        self.IP_ADDR = f'192.168.0.{int(node_id) + 1}'
        self.DATA_GRAVITY_TIMEOUT = data_gravity_request_timeout
        self.DATA_GRAVITY_MCAST = '224.0.0.251'
        self.MCAST_PORT = data_gravity_request_port
        self.SATELLITE_PORT = 50002
        self.model_path = model_path
        self.weight_path = weight_path
        self.dataset_path = dataset_path
        super().__init__(node_id)  # Call the constructor of the parent class (Node)

    def compute_data_gravity(self):
        """Compute Data Gravity in function of the dimension of the dataset."""
        with open(self.dataset_path, "rb") as ds:
            dim = 0
            while True:
                data = ds.read(1024)
                if not data:
                    break
                dim += len(data)
        self.data_gravity = dim / 1e15

    def request_data_gravity(self):
        """Send a data gravity request via UDP and receive responses from other nodes."""

        # Create a UDP socket for sending data gravity requests
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(self.IP_ADDR))

        # Message to broadcast
        message = b'\x47'

        try:
            # Send the message to the broadcast address and port
            udp_socket.sendto(message, (self.DATA_GRAVITY_MCAST, self.MCAST_PORT))
            self.logger.info(f"Data Gravity request sent at {self.DATA_GRAVITY_MCAST}:{self.MCAST_PORT}.")
        except socket.error as e:
            self.logger.debug("Socket error: ", e)

        udp_socket.settimeout(self.DATA_GRAVITY_TIMEOUT)

        nodes_gravities = []

        while True:
            try:
                # Receive responses to the data gravity request
                data, addr = udp_socket.recvfrom(4096)  # Adjust buffer size as needed
                if not data:
                    break
                # Deserialize the received data using pickle
                received_object = pickle.loads(data)

                if type(received_object) is tuple:
                    self.logger.info(f"received from: {addr} - Data Gravity: {received_object[1]}")
                    nodes_gravities.append((addr[0], received_object[0], received_object[1]))

            except socket.timeout:
                # Handle socket timeout (no data received within 10 seconds)
                self.logger.info(f"Timeout Responses.")
                break

            except socket.error as e:
                # Handle socket errors (e.g., if socket is closed)
                self.logger.debug("Socket error: ", e)
                self.logger.error("Socket error")

        udp_socket.close()
        return nodes_gravities

    def respond_data_gravity(self):
        """Start a UDP listener thread to respond to data gravity requests from other nodes."""

        # Clear the stop_receiver_flag to start the UDP listener thread
        self.stop_data_gravity_receiver_flag.clear()

        def udp_listener():
            # Create a UDP socket for listening to data gravity requests
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
            # udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
            udp_socket.bind((self.DATA_GRAVITY_MCAST, self.MCAST_PORT))  # Example UDP port

            #host = socket.gethostbyname(socket.gethostname())
            udp_socket.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(self.IP_ADDR))

            # mreq = struct.pack("4sl", socket.inet_aton(self.DATA_GRAVITY_MCAST), socket.INADDR_ANY)

            # udp_socket.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                                  socket.inet_aton(self.DATA_GRAVITY_MCAST) + socket.inet_aton(self.IP_ADDR))

            self.logger.info(f"Listening for Data Gravity requests on {self.DATA_GRAVITY_MCAST}:{self.MCAST_PORT}.")

            while not self.stop_data_gravity_receiver_flag.is_set():
                try:
                    # Receive data gravity requests from other nodes
                    data, addr = udp_socket.recvfrom(1)  # Adjust buffer size as needed

                    # Check if the received data contains the byte 0x47 (the equivalent char for 'G' as in 'Gravity')
                    if data == b'\x47':
                        # If the received byte matches, send the Data Gravity as response
                        tuple_to_send = (self.node_id, self.data_gravity)
                        serialized_data = pickle.dumps(tuple_to_send)
                        udp_socket.sendto(serialized_data, addr)
                        self.logger.info(f"Gravity sent at {addr[0]}:{addr[1]}.")
                    else:
                        # Handle other cases or ignore the data
                        self.logger.warning("Received unexpected data:", data)
                except socket.error as e:
                    # Handle socket errors (e.g., if socket is closed)
                    self.logger.debug("Socket error: ", e)
                    self.logger.error("Socket error")

        # Create and start the UDP listener thread
        self.data_gravity_receiver_thread = threading.Thread(target=udp_listener)
        self.data_gravity_receiver_thread.daemon = True  # Allow the program to exit when the main thread exits
        self.data_gravity_receiver_thread.start()

    def create_satellite(self, satellite_id, trip, jobs):
        """
        Create a new satellite with the given parameters.

        Args:
            satellite_id (str): The unique identifier for the satellite.
            trip (list): The trip plan for the satellite.
            jobs (list): The list of jobs to be performed by the satellite.

        Returns:
            Satellite: The created satellite object.
        """
        # Check if trip contains the current node_id and move it from current position to head
        for index, spot in enumerate(trip):
            if spot[1] == self.node_id:
                trip.insert(0, trip.pop(index))
                break

        # Create a new satellite with the specified parameters
        satellite = Satellite(creator_node_id=self.node_id, satellite_id=satellite_id, trip=trip, jobs=jobs)

        # Log information about the created satellite
        self.logger.info(f"Satellite {satellite.id} created.")
        self.logger.info(f"Satellite {satellite.id} destinations: {satellite.get_destinations_info()}")

        return satellite

    def append_satellite(self, satellite):
        """
        Append a satellite to the list of satellites.

        Args:
            satellite (Satellite): The satellite to be appended to the list.
        """
        # Single Thread access to append a satellite
        with self.satellite_lock:
            self.satellites.append(satellite)

    def append_completed_satellite(self, satellite):
        """
        Append a satellite to the list of completed satellites.

        Args:
            satellite (Satellite): The satellite to be appended to the list.
        """
        # Single Thread access to append a satellite
        with self.satellite_lock:
            self.completed_satellites.append(satellite)

    def pop_satellite(self):
        """
        Pop and return a satellite from the list of satellites.

        Returns:
            Satellite: The satellite removed from the list.
        """
        # Single Thread access to pop a satellite
        with self.satellite_lock:
            return self.satellites.pop()

    def execute_satellites(self, load_model_from_file=False):
        """
        Execute all satellites in the queue.

        Args:
            load_model_from_file (bool, optional): Whether to load the model from a file (default is False).
        """
        while self.satellites:
            satellite = self.pop_satellite()
            self.execute_satellite(satellite, load_model_from_file)
        self.logger.info(f"No satellites in the queue to be executed.")

    def execute_satellite(self, satellite, load_model_from_file=False):
        """
        Execute a satellite by performing specified jobs.

        Args:
            satellite (Satellite): The satellite to be executed.
            load_model_from_file (bool, optional): Whether to load the model from a file (default is False).
        """
        self.logger.info(f"Execution of satellite {satellite.id} started.")

        for job in satellite.jobs:
            if job == 'update':
                new_nodes_gravities = self.request_data_gravity()
                new_nodes_gravities.sort(key=lambda x: x[2], reverse=True)
                self.logger.info(satellite.update_trip(new_nodes_gravities))
            elif job == 'train':
                self.train_satellite(satellite, load_model_from_file)
            elif job == 'send':
                self.send_satellite(satellite)

        self.logger.info(f"Satellite {satellite.id} execution terminated.")

    def check_completed_satellites(self):
        """
        Checks if there are completed satellites in the queue.

        Returns:
            string: Number of completed satellites in queue.
        """
        self.logger.info(f"There are {len(self.completed_satellites)} completed satellites in queue.")
        return f"{len(self.completed_satellites)}"

    def train_satellite(self, satellite, load_model_from_file=False):
        """
        Train the model of a satellite.

        Args:
            satellite (Satellite): The satellite whose model is to be trained.
            load_model_from_file (bool, optional): Whether to load the model from a file (default is False).
        """
        if load_model_from_file:
            satellite.load_model(self.model_path, self.weight_path)
        self.logger.info(satellite.load_dataset(self.dataset_path))
        satellite.load_testset()

        satellite.train_model()
        self.logger.info(f"Satellite {satellite.id} model trained.")

        loss, acc, f1, roc = satellite.get_model_performance()

        self.logger.info(f"Satellite {satellite.id} performance: loss={loss} acc={acc} f1={f1} roc={roc}")

        buffer_entropy, classes_count = satellite.experience_replay()

        self.logger.info(f"Satellite {satellite.id} post experience replay - Buffer Entropy: {buffer_entropy} Classes Count: {classes_count}")

        loss, acc, f1, roc = satellite.get_model_performance()

        self.logger.info(f"Satellite {satellite.id} performance with Experience Replay: loss={loss} acc={acc} f1={f1} roc={roc}")

        satellite.unload_dataset()
        satellite.unload_testset()

        

    def receive_satellite(self):
        """
        Receive satellite data via a TCP listener and add it to the list of satellites.
        """
        # Clear the stop_receiver_flag to start the UDP listener thread
        self.stop_satellite_receiver_flag.clear()

        def tcp_listener():

            server_socket = None
            try:
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.bind(('0.0.0.0', self.SATELLITE_PORT))
                server_socket.listen(5)
                self.logger.info(f"Listening for Satellites landings on port {self.SATELLITE_PORT}.")
                while not self.stop_satellite_receiver_flag.is_set():
                    client_socket, client_address = server_socket.accept()
                    self.logger.info(f"Accepted connection from {client_address[0]}:{client_address[1]}")
                    # Start a new thread to handle the client
                    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
                    client_thread.start()
            except KeyboardInterrupt:
                self.logger.warning("Satellite Receiver stopped.")
            finally:
                if server_socket:
                    server_socket.close()

        def handle_client(client_socket):
            satellite = None
            try:
                data = []
                while True:
                    packet = client_socket.recv(4096)
                    if not packet:
                        break
                    data.append(packet)
                received_object = pickle.loads(b"".join(data))
                if isinstance(received_object, Satellite):
                    self.logger.info(f"Received satellite: {received_object}")
                    if received_object.is_train_completed():
                        self.append_completed_satellite(received_object)
                    else:
                        self.append_satellite(received_object)
                    self.logger.info(
                        f"Satellite {received_object.id} destinations: {received_object.get_destinations_info()}")
                else:
                    self.logger.warning("Received something, but wasn't a satellite. Landing Failed.")
            except Exception as e:
                self.logger.error(f"Error: {e}")
            finally:
                client_socket.close()


        # Create and start the TCP listener thread
        self.satellite_receiver_thread = threading.Thread(target=tcp_listener)
        self.satellite_receiver_thread.daemon = True  # Allow the program to exit when the main thread exits
        self.satellite_receiver_thread.start()

    def send_satellite(self, satellite):
        """
        Send a satellite to its next destination via a TCP connection.

        Args:
            satellite (Satellite): The satellite to be sent.
        """

        destination = satellite.get_next_destination()

        if destination is not None:
            satellite.set_new_actual_node()

        else:
            satellite.set_train_completed()
            destination = satellite.get_home_destination()
            self.logger.info(f"Satellite {satellite.id} reached final node. Sending satellite back to home: "
                             f"{destination}")

        client_socket = None
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((destination, self.SATELLITE_PORT))
            self.logger.info(f"Connected to server at {destination}:{self.SATELLITE_PORT}")

            # Serialize and send the Python object using pickle
            serialized_data = pickle.dumps(satellite)
            while True:
                try:
                    client_socket.sendall(serialized_data)
                except ConnectionError:
                    self.logger.error(f"Impossible to establish a connection with {destination}, retyring!")
                else:
                    break
                
            self.logger.info(f"Sent on network {len(serialized_data)} for Satellite {satellite.id}.")
        except KeyboardInterrupt:
            self.logger.warning("Client disconnected.")
        finally:
            if client_socket:
                client_socket.close()

        self.logger.info(f"Satellite {satellite.id} sent at {destination}.")

    def respond_join(self):
        """Wait for the UDP listener thread to join (terminate)."""
        self.data_gravity_receiver_thread.join()

    def debug_info(self):
        """Return debug information about the node, including data gravity."""
        info = ""
        info += f"Data Gravity:\t{self.data_gravity}\n"
        self.logger.debug(info)


if __name__ == "__main__":
    pass
