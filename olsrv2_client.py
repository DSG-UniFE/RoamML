import socket
import logging
from typing import Optional

HOST = "localhost"
PORT = 2009

def connect(host: str, port: int) -> socket.socket:
    """Connect to olsrv2 server and return socket object"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def send_command(command: str, host: Optional[str] = "localhost", port: Optional[int] = 2009) -> str:
    """Send command to telnet server and return the result
    Read untile the prompt is asking for a new command"""
    s = connect(host, port)
    s.sendall(command.encode('ascii') + b"\n")
    ### Read until the prompt is asking for a new command
    data = s.recv(1024)
    res = data.decode('ascii')
    while not res.endswith("> "):
        data = s.recv(1024)
        res += data.decode('ascii')
    """ Send the exit command to close the connection """
    try:
        s.sendall(b"exit\n")
        s.close()
    except Exception as e:
        logging.error("Exception while closing the connection: %s", e)
    return res

def parse_nhdpinfo_result(result: str) -> list:
    """Parse the result of nhdpinfo neighbor command
       Parse the content of each line and put it a dictionary
       The dictionary is added to a list. This is an example of a line:
    192.168.0.4     2001::3 true    1       0       ff_dat_metric   1.02kbit/s     2105088  1.02kbit/s      2105088 mpr     false   true    7
    """
    nodes = []
    for nodestr in result.splitlines():
        line = nodestr.split()
        if line == []: break
        node = {}
        node['ip'] = line[0]
        node['ipv6'] = line[1]
        node['symmetric'] = line[2]
        node['hysteresis'] = line[3]
        node['willingness'] = line[4]
        node['dat_metric'] = line[5]
        node['dat_metric_value'] = line[6]
        node['dat_metric_value_raw'] = line[7]
        node['dat_metric_value_raw'] = line[8]
        node['mpr'] = line[9]
        node['mpr_selector'] = line[10]
        node['mpr_willingness'] = line[11]
        node['link_quality'] = line[12]
        nodes.append(node)
    return nodes

def get_neighbors_info(host: str, port: int) -> list:
    """Connect to telnet server and send the nhdpinfo neighbor command"""
    res = send_command("nhdpinfo neighbor")
    logging.debug(res)
    nodes = parse_nhdpinfo_result(res)
    return nodes

def parse_olsrv2_routes(result: str) -> list:
    """Parse the results of the olsrv2info route command
    Each line contains a route information and is formatted as follows:
    192.168.0.2     -       192.168.0.1     0.0.0.0/0       2       254     100     sta1-wlan0      266     192.168.0.1     0   ff_dat_metric    58.04Mbit/s (1 hops)    37      1
    This method parses the line and adds the information to a dictionary
    In the example above (1 hops) should be parsed as with key hops and value 1:
    result: the result of the olsrv2info route command; contains multiple lines
    """
    nodes = []
    for nodestr in result.splitlines():
        line = nodestr.split()
        if line == []: break
        node = {}
        node['originator'] = line[0]
        node['destination'] = line[2]
        node['prefix'] = line[3]
        node['distance'] = line[4]
        node['last'] = line[5]
        node['validity'] = line[6]
        node['interface'] = line[7]
        node['metric'] = line[8]
        node['nexthop'] = line[9]
        node['nexthop_type'] = line[10]
        node['dat_metric'] = line[11]
        node['dat_metric_value'] = line[12]
        node['hops'] = line[13].removeprefix('(').removesuffix(')')
        nodes.append(node)
    return nodes

def get_olsrv2_routes(host: str, port: int) -> list:
    """Connect to telnet server and send the nhdpinfo neighbor command"""
    res = send_command("olsrv2info route")
    logging.debug(res)
    nodes = parse_olsrv2_routes(res)
    return nodes

def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Starting -- nhdpinfo neighbor")
    nodes = get_neighbors_info(HOST, PORT)
    logging.debug(nodes)
    logging.debug("Starting -- olsrv2info route")
    nodes = get_olsrv2_routes(HOST, PORT)
    logging.debug(nodes)

    print(nodes)

if __name__ == "__main__":
    main()