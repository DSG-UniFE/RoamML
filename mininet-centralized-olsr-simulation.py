#!/usr/bin/env python

"""This example shows how to enable 4-address
Warning: It works only when network manager is stopped"""

import sys
import time

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, _4address, adhoc
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mininet.term import makeTerms, makeTerm


def topology(args):
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    # X = [8, 3.64, 17.45, 15.26, 15.2, 5.98, 7.96, 9.71, 4.78, 15.75]
    # Y = [26, 7.21, 20.99, 15.9, 5.73, 9.82, 20.21, 4.49, 14.13, 12.55]
    # Z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    X = [8.00, 3.64, 17.45, 15.26, 15.20, 5.98, 7.96, 9.71, 4.78, 15.75, 12.00, 14.00, 9.00, 18.00, 10.00, 13.37, 11.23]
    Y = [26.00, 7.21, 20.99, 15.90, 5.73, 9.82, 20.21, 4.49, 14.13, 12.55, 22.00, 13.00, 16.00, 8.00, 19.00, 14.56, 16.78]
    Z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


    positions = []

    for x, y, z in zip(X, Y, Z):
        positions.append(f'{x*8},{y*8},{z}')

    info("*** Creating nodes\n")

    sta1 = net.addStation('sta1', ip="192.168.0.1/24", position=positions[0])
    sta2 = net.addStation('sta2', ip="192.168.0.2/24", position=positions[1])
    sta3 = net.addStation('sta3', ip="192.168.0.3/24", position=positions[2])
    sta4 = net.addStation('sta4', ip="192.168.0.4/24", position=positions[3])
    sta5 = net.addStation('sta5', ip="192.168.0.5/24", position=positions[4])
    sta6 = net.addStation('sta6', ip="192.168.0.6/24", position=positions[5])
    sta7 = net.addStation('sta7', ip="192.168.0.7/24", position=positions[6])
    sta8 = net.addStation('sta8', ip="192.168.0.8/24", position=positions[7])
    sta9 = net.addStation('sta9', ip="192.168.0.9/24", position=positions[8])
    sta10 = net.addStation('sta10', ip="192.168.0.10/24", position=positions[9])
    sta11 = net.addStation('sta11', ip="192.168.0.11/24", position=positions[10])
    sta12 = net.addStation('sta12', ip="192.168.0.12/24", position=positions[11])
    sta13 = net.addStation('sta13', ip="192.168.0.13/24", position=positions[12])
    sta14 = net.addStation('sta14', ip="192.168.0.14/24", position=positions[13])
    sta15 = net.addStation('sta15', ip="192.168.0.15/24", position=positions[14])



    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3.5)

    info("*** Configuring nodes\n")
    net.configureNodes()

    # proto = 'batmand'
    proto = 'olsrd2'

    info("*** Adding Links\n")
    net.addLink(sta1, cls=adhoc, intf='sta1-wlan0',
                ssid='adhocNet', proto=proto,
                mode='g', channel=5)
    net.addLink(sta2, cls=adhoc, intf='sta2-wlan0',
                ssid='adhocNet', proto=proto,
                mode='g', channel=5)
    net.addLink(sta3, cls=adhoc, intf='sta3-wlan0',
                ssid='adhocNet', proto=proto,
                mode='g', channel=5)
    net.addLink(sta4, cls=adhoc, intf='sta4-wlan0',
                ssid='adhocNet', proto=proto,
                mode='g', channel=5)
    net.addLink(sta5, cls=adhoc, intf='sta5-wlan0',
                ssid='adhocNet', proto=proto,
                mode='g', channel=5)
    net.addLink(sta6, cls=adhoc, intf='sta6-wlan0',
                ssid='adhocNet', proto=proto,
                mode='g', channel=5)
    net.addLink(sta7, cls=adhoc, intf='sta7-wlan0',
                ssid='adhocNet', proto=proto,
                mode='g', channel=5)
    net.addLink(sta8, cls=adhoc, intf='sta8-wlan0',
                ssid='adhocNet', proto=proto,
                mode='g', channel=5)
    net.addLink(sta9, cls=adhoc, intf='sta9-wlan0',
                ssid='adhocNet', proto=proto,
                mode='g', channel=5)
    net.addLink(sta10, cls=adhoc, intf='sta10-wlan0',
                ssid='adhocNet', proto=proto,
                mode='g', channel=5)
    net.addLink(sta11, cls=adhoc, intf='sta11-wlan0',
                ssid='adhocNet', proto=proto,
                mode='g', channel=5)
    net.addLink(sta12, cls=adhoc, intf='sta12-wlan0',
                ssid='adhocNet', proto=proto,
                mode='g', channel=5)
    net.addLink(sta13, cls=adhoc, intf='sta13-wlan0',
                ssid='adhocNet', proto=proto,
                mode='g', channel=5)
    net.addLink(sta14, cls=adhoc, intf='sta14-wlan0',
                ssid='adhocNet', proto=proto,
                mode='g', channel=5)
    net.addLink(sta15, cls=adhoc, intf='sta15-wlan0',
                ssid='adhocNet', proto=proto,
                mode='g', channel=5)



    if '-p' not in args:
        net.plotGraph(max_x=300, max_y=300)

    info("*** Starting network\n")
    # net.setMobilityModel(time=0, model='RandomDirection', max_x=300, max_y=300, seed=20)
    net.build()

    info("\n*** Starting olsrd with dedicated config file\n")
    sta1.cmd("olsrd -f olsrd_config_files/olsrd_node1.conf > /dev/null 2>&1 & ")
    sta2.cmd("olsrd -f olsrd_config_files/olsrd_node2.conf > /dev/null 2>&1 & ")
    sta3.cmd("olsrd -f olsrd_config_files/olsrd_node3.conf > /dev/null 2>&1 & ")
    sta4.cmd("olsrd -f olsrd_config_files/olsrd_node4.conf > /dev/null 2>&1 & ")
    sta5.cmd("olsrd -f olsrd_config_files/olsrd_node5.conf > /dev/null 2>&1 & ")
    sta6.cmd("olsrd -f olsrd_config_files/olsrd_node6.conf > /dev/null 2>&1 & ")
    sta7.cmd("olsrd -f olsrd_config_files/olsrd_node7.conf > /dev/null 2>&1 & ")
    sta8.cmd("olsrd -f olsrd_config_files/olsrd_node8.conf > /dev/null 2>&1 & ")
    sta9.cmd("olsrd -f olsrd_config_files/olsrd_node9.conf > /dev/null 2>&1 & ")
    sta10.cmd("olsrd -f olsrd_config_files/olsrd_node10.conf > /dev/null 2>&1 & ")
    sta11.cmd("olsrd -f olsrd_config_files/olsrd_node11.conf > /dev/null 2>&1 & ")
    sta12.cmd("olsrd -f olsrd_config_files/olsrd_node12.conf > /dev/null 2>&1 & ")
    sta13.cmd("olsrd -f olsrd_config_files/olsrd_node13.conf > /dev/null 2>&1 & ")
    sta14.cmd("olsrd -f olsrd_config_files/olsrd_node14.conf > /dev/null 2>&1 & ")
    sta15.cmd("olsrd -f olsrd_config_files/olsrd_node15.conf > /dev/null 2>&1 & ")
    time.sleep(5)

    info("\n*** TCPDUMP\n")
    sta1.cmd("tcpdump -w sta1-centralized_capture.pcap port 50055 -i sta1-wlan0 > /dev/null 2>&1 & ")
    sta2.cmd("tcpdump -w sta2-centralized_capture.pcap port 50055 -i sta2-wlan0 > /dev/null 2>&1 & ")
    sta3.cmd("tcpdump -w sta3-centralized_capture.pcap port 50055 -i sta3-wlan0 > /dev/null 2>&1 & ")
    sta4.cmd("tcpdump -w sta4-centralized_capture.pcap port 50055 -i sta4-wlan0 > /dev/null 2>&1 & ")
    sta5.cmd("tcpdump -w sta5-centralized_capture.pcap port 50055 -i sta5-wlan0 > /dev/null 2>&1 & ")
    sta6.cmd("tcpdump -w sta6-centralized_capture.pcap port 50055 -i sta6-wlan0 > /dev/null 2>&1 & ")
    sta7.cmd("tcpdump -w sta7-centralized_capture.pcap port 50055 -i sta7-wlan0 > /dev/null 2>&1 & ")
    sta8.cmd("tcpdump -w sta8-centralized_capture.pcap port 50055 -i sta8-wlan0 > /dev/null 2>&1 & ")
    sta9.cmd("tcpdump -w sta9-centralized_capture.pcap port 50055 -i sta9-wlan0 > /dev/null 2>&1 & ")
    sta10.cmd("tcpdump -w sta10-centralized_capture.pcap port 50055 -i sta10-wlan0 > /dev/null 2>&1 & ")
    sta11.cmd("tcpdump -w sta11-centralized_capture.pcap port 50055 -i sta11-wlan0 > /dev/null 2>&1 & ")
    sta12.cmd("tcpdump -w sta12-centralized_capture.pcap port 50055 -i sta12-wlan0 > /dev/null 2>&1 & ")
    sta13.cmd("tcpdump -w sta13-centralized_capture.pcap port 50055 -i sta13-wlan0 > /dev/null 2>&1 & ")
    sta14.cmd("tcpdump -w sta14-centralized_capture.pcap port 50055 -i sta14-wlan0 > /dev/null 2>&1 & ")
    sta15.cmd("tcpdump -w sta15-centralized_capture.pcap port 50055 -i sta15-wlan0 > /dev/null 2>&1 & ")
    time.sleep(5)


    info("\n*** simulation\n")
    sta1.cmd("venv/bin/python centralized_receiver.py > receiver.log 2>&1 & ")

    sta2.cmd("venv/bin/python centralized_sender.py 192.168.0.1 1 > sender_1.log 2>&1 & ")
    sta3.cmd("venv/bin/python centralized_sender.py 192.168.0.1 2 > sender_2.log 2>&1 & ")
    sta4.cmd("venv/bin/python centralized_sender.py 192.168.0.1 3 > sender_3.log 2>&1 & ")
    sta5.cmd("venv/bin/python centralized_sender.py 192.168.0.1 4 > sender_4.log 2>&1 & ")
    sta6.cmd("venv/bin/python centralized_sender.py 192.168.0.1 5 > sender_5.log 2>&1 & ")
    sta7.cmd("venv/bin/python centralized_sender.py 192.168.0.1 6 > sender_6.log 2>&1 & ")
    sta8.cmd("venv/bin/python centralized_sender.py 192.168.0.1 7 > sender_7.log 2>&1 & ")
    sta9.cmd("venv/bin/python centralized_sender.py 192.168.0.1 8 > sender_8.log 2>&1 & ")
    sta10.cmd("venv/bin/python centralized_sender.py 192.168.0.1 9 > sender_9.log 2>&1 & ")
    sta11.cmd("venv/bin/python centralized_sender.py 192.168.0.1 10 > sender_10.log 2>&1 & ")
    sta12.cmd("venv/bin/python centralized_sender.py 192.168.0.1 11 > sender_11.log 2>&1 & ")
    sta13.cmd("venv/bin/python centralized_sender.py 192.168.0.1 12 > sender_12.log 2>&1 & ")
    sta14.cmd("venv/bin/python centralized_sender.py 192.168.0.1 13 > sender_13.log 2>&1 & ")
    sta15.cmd("venv/bin/python centralized_sender.py 192.168.0.1 14 > sender_14.log 2>&1 & ")


    # makeTerm(node=sta1, title='sta1', cmd="bash -c 'source venv/bin/activate; python centralized_receiver.py'")
    # makeTerm(node=sta2, title='sta2', cmd="bash -c 'source venv/bin/activate; python centralized_sender.py 192.168.0.1 1'")
    # makeTerm(node=sta3, title='sta3', cmd="bash -c 'source venv/bin/activate; python centralized_sender.py 192.168.0.1 2'")
    # makeTerm(node=sta4, title='sta4', cmd="bash -c 'source venv/bin/activate; python centralized_sender.py 192.168.0.1 3'")
    # makeTerm(node=sta5, title='sta5', cmd="bash -c 'source venv/bin/activate; python centralized_sender.py 192.168.0.1 4'")
    # makeTerm(node=sta6, title='sta6', cmd="bash -c 'source venv/bin/activate; python centralized_sender.py 192.168.0.1 5'")
    # makeTerm(node=sta7, title='sta7', cmd="bash -c 'source venv/bin/activate; python centralized_sender.py 192.168.0.1 6'")
    # makeTerm(node=sta8, title='sta8', cmd="bash -c 'source venv/bin/activate; python centralized_sender.py 192.168.0.1 7'")
    # makeTerm(node=sta9, title='sta9', cmd="bash -c 'source venv/bin/activate; python centralized_sender.py 192.168.0.1 8'")
    # makeTerm(node=sta10, title='sta10', cmd="bash -c 'source venv/bin/activate; python centralized_sender.py 192.168.0.1 9'")
    # makeTerm(node=sta11, title='sta11',
    #          cmd="bash -c 'source venv/bin/activate; python centralized_sender.py 192.168.0.1 0'")


    # makeTerm(node=ap1, title='ap1', cmd="bash -c 'tcpdump -w recevier_capture.pcap -i ap1-wlan1 port 50055'")

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
