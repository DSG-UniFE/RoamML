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

    X = [8, 3.64, 17.45, 15.26, 15.2, 5.98, 7.96, 9.71, 4.78, 15.75]
    Y = [26, 7.21, 20.99, 15.9, 5.73, 9.82, 20.21, 4.49, 14.13, 12.55]
    Z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    positions = []

    for x, y, z in zip(X, Y, Z):
        positions.append(f'{x*10},{y*10},{z}')

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



    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4)

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

    if '-p' not in args:
        net.plotGraph(max_x=300, max_y=300)

    info("*** Starting network\n")
    # net.setMobilityModel(time=0, model='RandomDirection', max_x=300, max_y=300, seed=20)
    net.build()

    info("\n*** Starting olsrd with dedicated config file\n")
    sta1.cmd("olsrd -f olsrd_config_files/olsrd_node1.conf > /dev/null 2> /dev/null & ")
    sta2.cmd("olsrd -f olsrd_config_files/olsrd_node2.conf > /dev/null 2> /dev/null & ")
    sta3.cmd("olsrd -f olsrd_config_files/olsrd_node3.conf > /dev/null 2> /dev/null & ")
    sta4.cmd("olsrd -f olsrd_config_files/olsrd_node4.conf > /dev/null 2> /dev/null & ")
    sta5.cmd("olsrd -f olsrd_config_files/olsrd_node5.conf > /dev/null 2> /dev/null & ")
    sta6.cmd("olsrd -f olsrd_config_files/olsrd_node6.conf > /dev/null 2> /dev/null & ")
    sta7.cmd("olsrd -f olsrd_config_files/olsrd_node7.conf > /dev/null 2> /dev/null & ")
    sta8.cmd("olsrd -f olsrd_config_files/olsrd_node8.conf > /dev/null 2> /dev/null & ")
    sta9.cmd("olsrd -f olsrd_config_files/olsrd_node9.conf > /dev/null 2> /dev/null & ")
    sta10.cmd("olsrd -f olsrd_config_files/olsrd_node10.conf > /dev/null 2> /dev/null & ")
    time.sleep(5)

    info("*** Starting simulation\n")
    makeTerm(node=sta1, title='sta1', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 0'")
    makeTerm(node=sta2, title='sta2', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 1'")
    makeTerm(node=sta3, title='sta3', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 2'")
    makeTerm(node=sta4, title='sta4', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 3'")
    makeTerm(node=sta5, title='sta5', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 4'")
    makeTerm(node=sta6, title='sta6', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 5'")
    makeTerm(node=sta7, title='sta7', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 6'")
    makeTerm(node=sta8, title='sta8', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 7'")
    makeTerm(node=sta9, title='sta9', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 8'")
    makeTerm(node=sta10, title='sta10', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 9'")


    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
