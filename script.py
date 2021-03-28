#!/usr/bin/python

from __future__ import print_function

import os
from mininet.topo import Topo # Topo : the base class for Mininet topologies
from mininet.net import Mininet # Mininet : main class to create and manage a network
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import Intf
from mininet.node import Controller

class NetworkTopo( Topo ):
    # Builds network topology with a loop 
    # The method to override in your topology class.
    # Constructor parameters (n) will be passed through to it automatically by Topo.__init__(). 
    # This method creates a template (basically a graph of node names, and a database of configuration information)
    # which is then used by Mininet to create the actual topology.
    def build( self, **_opts ):

        # Adding legacy switches
        s1, s2, s3 = [ self.addSwitch( s, failMode='standalone' ) # addSwitch : adds a switch to a Topo and returns the switch name
                   for s in ( 's1', 's2', 's3' ) ]
        
        # Creating links
        self.addLink( s1, s2 )
        self.addLink( s2, s3 )
        self.addLink( s3, s1 )

        # Adding hosts
        h1 = self.addHost( 'h1' ) # adds a host to a Topo and returns the host name
        h2 = self.addHost( 'h2' )
        h3 = self.addHost( 'h3' )
        h4 = self.addHost( 'h4' )
        h5 = self.addHost( 'h5' )
        h6 = self.addHost( 'h6' )
        
        # Connecting hosts to switches
        for h, s in [ (h1, s1), (h2, s1), (h3, s2), (h4, s2), (h5, s3), (h6, s3) ]:
            self.addLink( h, s ) # adds a bidirectional link to Topo. Links in Mininet are bidirectional unless noted otherwise.


def run():

    topo = NetworkTopo() 

    # Different topologies configures by default : 
        # SingleSwitchTopo() | Description : Single Switch Connected to k hosts
        # SingleSwitchReversedTopo() | Description : Single switch connected to k hosts, with reversed ports.
        # MinimalTopo() | Description : Minimal topology with two hosts and one switch
        # LinearTopo() | Descripton : Linear topology of k switches, with n hosts per switch.
    net = Mininet( topo=topo, controller=None)
    # Mininet() is the constructor that creates and returns a Mininet network object. 
        # It takes a number of configuration parameters, notably:
            # topo: a topology object (not a constructor or template - the actual object!)
            # host: a constructor used to create Host elements in the topology
            # switch: a constructor used to create Switch elements in the topology
            # controller: a constructor used to create Controller elements in the topology
            # link: a constructor used to create Links in the topology

    net.start() # start() starts your network 
    net['s1'].cmd('ovs-vsctl set bridge s1 stp-enable=true') 
    net['s2'].cmd('ovs-vsctl set bridge s2 stp-enable=true')
    net['s3'].cmd('ovs-vsctl set bridge s3 stp-enable=true')
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
