# Software-Defined Networking

## Why SDN

"Software-Defined Networking (SDN)" is a term of the programmable networks paradigm. (A paradigm is a standard, perspective, or set of ideas.)

In short, SDN refers to the ability of software applications to program individual network devices dynamically and therefore control the behavior of the network as a whole.

SDN separates the network’s control (brains) and forwarding (muscle) planes and provides a centralized view of the distributed network for more efficient orchestration and automation of network services.

The SDN architecture is:

- Directly programmable: Network control is directly programmable because it is decoupled from forwarding functions.
- Agile: Abstracting control from forwarding lets administrators dynamically adjust network-wide [traffic flow](https://en.wikipedia.org/wiki/Traffic_flow_(computer_networking)) to meet changing needs.
- Centrally managed: Network intelligence is (logically) centralized in software-based SDN controllers that maintain a global view of the network, which appears to applications and policy engines as a single, logical switch.
- Programmatically configured: SDN lets network managers configure, manage, secure, and optimize network resources very quickly via dynamic, automated SDN programs, which they can write themselves because the programs do not depend on proprietary software.
- Open standards-based and vendor-neutral: When implemented through open standards, SDN simplifies network design and operation because instructions are provided by SDN controllers instead of multiple, vendor-specific devices and protocols.

![sdn](/assets/sdn.webp)

## REST API

In case you are not familiar with REST API, check this github repository where I explained what is REST API using a simple flask app : [REST API](https://github.com/seifallahhomrani1/api)

## OpenDaylight Controller

The OpenDaylight Project is a collaborative open-source project hosted by The Linux Foundation. The project serves as a platform for software-defined networking (SDN) for open, centralized, network device monitoring.

> I've used Opendaylight Controller as a service inside a ubuntu VM with the hep of this awesome [article](https://john.soban.ski/how-to-install-opendaylight-as-a-service-on-ubuntu.html) by John Sobanski.

## Mininet

Mininet creates a realistic virtual network, running real kernel, switch and application code, on a single machine (VM, cloud or native), in seconds.

The script I used to create a personalized network in mininet using python can be found [here](script.py).

## Using the OpenDaylight SDN Controller with the Mininet

I've recently found [this awesome article](https://www.brianlinkletter.com/2016/02/using-the-opendaylight-sdn-controller-with-the-mininet-network-emulator/) by Brian Linkletter which explains how to integrate ODL with Mininet.

## OpenFlow Manager

After configuring the SDN and running the basic configurations, I needed an app to be running in top of ODL, and here I used the [OpenFlow Manager](https://github.com/CiscoDevNet/OpenDaylight-Openflow-App) (link refers to the OFM github repository) which is an application developed to run on top of ODL to visualize OpenFlow (OF) topologies, program OF paths and gather OF stats.

![OFM](/assets/OFM.png)

## Other Resources

[RFC 7426](https://tools.ietf.org/html/rfc7426)
