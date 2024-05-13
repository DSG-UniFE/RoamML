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
        positions.append(f'{x*12},{y*12},{z}')

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

    #proto = 'batmand'
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
        net.plotGraph(max_x=800, max_y=800)

    info("*** Starting network\n")
    # net.setMobilityModel(time=0, model='RandomDirection', max_x=300, max_y=300, seed=20)
    net.build()

    info("\n*** Starting olsrd with dedicated config file\n")
    sta1.cmd("olsrd2_static sta1-wlan0 > /dev/null 2>&1 & ")
    sta2.cmd("olsrd2_static sta2-wlan0 > /dev/null 2>&1 & ")
    sta3.cmd("olsrd2_static sta3-wlan0 > /dev/null 2>&1 & ")
    sta4.cmd("olsrd2_static sta4-wlan0 > /dev/null 2>&1 & ")
    sta5.cmd("olsrd2_static sta5-wlan0 > /dev/null 2>&1 & ")
    sta6.cmd("olsrd2_static sta6-wlan0 > /dev/null 2>&1 & ")
    sta7.cmd("olsrd2_static sta7-wlan0 > /dev/null 2>&1 & ")
    sta8.cmd("olsrd2_static sta8-wlan0  > /dev/null 2>&1 & ")
    sta9.cmd("olsrd2_static sta9-wlan0  > /dev/null 2>&1 & ")
    sta10.cmd("olsrd2_static sta10-wlan0 > /dev/null 2>&1 & ")
    sta11.cmd("olsrd2_static sta11-wlan0 > /dev/null 2>&1 & ")
    sta12.cmd("olsrd2_static sta12-wlan0 > /dev/null 2>&1 & ")
    sta13.cmd("olsrd2_static sta13-wlan0 > /dev/null 2>&1 & ")
    sta14.cmd("olsrd2_static sta14-wlan0 > /dev/null 2>&1 & ")
    sta15.cmd("olsrd2_static sta15-wlan0 > /dev/null 2>&1 & ")
    time.sleep(5)

    if "-s" not in args:
        info("*** Starting tcpdump\n")
        sta1.cmd("tcpdump -w sta1-gravity_capture.pcap port 50001 -i sta1-wlan0 > /dev/null 2>&1 & ")
        sta2.cmd("tcpdump -w sta2-gravity_capture.pcap port 50001 -i sta2-wlan0 > /dev/null 2>&1 & ")
        sta3.cmd("tcpdump -w sta3-gravity_capture.pcap port 50001 -i sta3-wlan0 > /dev/null 2>&1 & ")
        sta4.cmd("tcpdump -w sta4-gravity_capture.pcap port 50001 -i sta4-wlan0 > /dev/null 2>&1 & ")
        sta5.cmd("tcpdump -w sta5-gravity_capture.pcap port 50001 -i sta5-wlan0 > /dev/null 2>&1 & ")
        sta6.cmd("tcpdump -w sta6-gravity_capture.pcap port 50001 -i sta6-wlan0 > /dev/null 2>&1 & ")
        sta7.cmd("tcpdump -w sta7-gravity_capture.pcap port 50001 -i sta7-wlan0 > /dev/null 2>&1 & ")
        sta8.cmd("tcpdump -w sta8-gravity_capture.pcap port 50001 -i sta8-wlan0 > /dev/null 2>&1 & ")
        sta9.cmd("tcpdump -w sta9-gravity_capture.pcap port 50001 -i sta9-wlan0 > /dev/null 2>&1 & ")
        sta10.cmd("tcpdump -w sta10-gravity_capture.pcap port 50001 -i sta10-wlan0 > /dev/null 2>&1 & ")
        sta11.cmd("tcpdump -w sta11-gravity_capture.pcap port 50001 -i sta11-wlan0 > /dev/null 2>&1 & ")
        sta12.cmd("tcpdump -w sta12-gravity_capture.pcap port 50001 -i sta12-wlan0 > /dev/null 2>&1 & ")
        sta13.cmd("tcpdump -w sta13-gravity_capture.pcap port 50001 -i sta13-wlan0 > /dev/null 2>&1 & ")
        sta14.cmd("tcpdump -w sta14-gravity_capture.pcap port 50001 -i sta14-wlan0 > /dev/null 2>&1 & ")
        sta15.cmd("tcpdump -w sta15-gravity_capture.pcap port 50001 -i sta15-wlan0 > /dev/null 2>&1 & ")

        sta1.cmd("tcpdump -w sta1-satellite_capture.pcap port 50002 -i sta1-wlan0 > /dev/null 2>&1 & ")
        sta2.cmd("tcpdump -w sta2-satellite_capture.pcap port 50002 -i sta2-wlan0 > /dev/null 2>&1 & ")
        sta3.cmd("tcpdump -w sta3-satellite_capture.pcap port 50002 -i sta3-wlan0 > /dev/null 2>&1 & ")
        sta4.cmd("tcpdump -w sta4-satellite_capture.pcap port 50002 -i sta4-wlan0 > /dev/null 2>&1 & ")
        sta5.cmd("tcpdump -w sta5-satellite_capture.pcap port 50002 -i sta5-wlan0 > /dev/null 2>&1 & ")
        sta6.cmd("tcpdump -w sta6-satellite_capture.pcap port 50002 -i sta6-wlan0 > /dev/null 2>&1 & ")
        sta7.cmd("tcpdump -w sta7-satellite_capture.pcap port 50002 -i sta7-wlan0 > /dev/null 2>&1 & ")
        sta8.cmd("tcpdump -w sta8-satellite_capture.pcap port 50002 -i sta8-wlan0 > /dev/null 2>&1 & ")
        sta9.cmd("tcpdump -w sta9-satellite_capture.pcap port 50002 -i sta9-wlan0 > /dev/null 2>&1 & ")
        sta10.cmd("tcpdump -w sta10-satellite_capture.pcap port 50002 -i sta10-wlan0 > /dev/null 2>&1 & ")
        sta11.cmd("tcpdump -w sta11-satellite_capture.pcap port 50002 -i sta11-wlan0 > /dev/null 2>&1 & ")
        sta12.cmd("tcpdump -w sta12-satellite_capture.pcap port 50002 -i sta12-wlan0 > /dev/null 2>&1 & ")
        sta13.cmd("tcpdump -w sta13-satellite_capture.pcap port 50002 -i sta13-wlan0 > /dev/null 2>&1 & ")
        sta14.cmd("tcpdump -w sta14-satellite_capture.pcap port 50002 -i sta14-wlan0 > /dev/null 2>&1 & ")
        sta15.cmd("tcpdump -w sta15-satellite_capture.pcap port 50002 -i sta15-wlan0 > /dev/null 2>&1 & ")

        time.sleep(5)

        info("*** Starting simulation\n")

        sta1.cmd("venv/bin/python satellite_data_simulation.py 0 > nodeouterr00.log 2>&1 & ")
        sta2.cmd("venv/bin/python satellite_data_simulation.py 1 > nodeouterr01.log 2>&1 & ")
        sta3.cmd("venv/bin/python satellite_data_simulation.py 2 > nodeouterr02.log 2>&1 & ")
        sta4.cmd("venv/bin/python satellite_data_simulation.py 3 > nodeouterr03.log 2>&1 & ")
        sta5.cmd("venv/bin/python satellite_data_simulation.py 4 > nodeouterr04.log 2>&1 & ")
        sta6.cmd("venv/bin/python satellite_data_simulation.py 5 > nodeouterr05.log 2>&1 & ")
        sta7.cmd("venv/bin/python satellite_data_simulation.py 6 > nodeouterr06.log 2>&1 & ")
        sta8.cmd("venv/bin/python satellite_data_simulation.py 7 > nodeouterr07.log 2>&1 & ")
        sta9.cmd("venv/bin/python satellite_data_simulation.py 8 > nodeouterr08.log 2>&1 & ")
        sta10.cmd("venv/bin/python satellite_data_simulation.py 9 > nodeouterr09.log 2>&1 & ")
        sta11.cmd("venv/bin/python satellite_data_simulation.py 10 > nodeouterr10.log 2>&1 & ")
        sta12.cmd("venv/bin/python satellite_data_simulation.py 11 > nodeouterr11.log 2>&1 & ")
        sta13.cmd("venv/bin/python satellite_data_simulation.py 12 > nodeouterr12.log 2>&1 & ")
        sta14.cmd("venv/bin/python satellite_data_simulation.py 13 > nodeouterr13.log 2>&1 & ")
        sta15.cmd("venv/bin/python satellite_data_simulation.py 14 > nodeouterr14.log 2>&1 & ")

    # makeTerm(node=sta1, title='node 0 - 192.168.0.1', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 0'")
    # makeTerm(node=sta2, title='node 1 - 192.168.0.2', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 1'")
    # makeTerm(node=sta3, title='node 2 - 192.168.0.3', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 2'")
    # makeTerm(node=sta4, title='node 3 - 192.168.0.4', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 3'")
    # makeTerm(node=sta5, title='node 4 - 192.168.0.5', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 4'")
    # makeTerm(node=sta6, title='node 5 - 192.168.0.6', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 5'")
    # makeTerm(node=sta7, title='node 6 - 192.168.0.7', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 6'")
    # makeTerm(node=sta8, title='node 7 - 192.168.0.8', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 7'")
    # makeTerm(node=sta9, title='node 8 - 192.168.0.9', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 8'")
    # makeTerm(node=sta10, title='node 9 - 192.168.0.10', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 9'")
    # makeTerm(node=sta11, title='node 10 - 192.168.0.11', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 10'")
    # makeTerm(node=sta12, title='node 11 - 192.168.0.12', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 11'")
    # makeTerm(node=sta13, title='node 12 - 192.168.0.13', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 12'")
    # makeTerm(node=sta14, title='node 13 - 192.168.0.14', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 13'")
    # makeTerm(node=sta15, title='node 14 - 192.168.0.15', cmd="bash -c 'source venv/bin/activate; python satellite_data_simulation.py 14'")

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
