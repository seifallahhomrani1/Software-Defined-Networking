---
toc : true
---

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

![sdn](sdn.webp)

## SDN History

<iframe width="560" height="315" src="https://www.youtube.com/embed/4Cb91JT-Xb4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


## REST API

In case you are not familiar with REST API, check this github repository where I explained what is REST API using a simple flask app : [REST API](https://github.com/seifallahhomrani1/api)

## OpenDaylight Controller

The OpenDaylight Project is a collaborative open-source project hosted by The Linux Foundation. The project serves as a platform for software-defined networking (SDN) for open, centralized, network device monitoring.


## Mininet

Mininet creates a realistic virtual network, running real kernel, switch and application code, on a single machine (VM, cloud or native), in seconds.

The script I used to create a personalized network in mininet using python can be found [here](script.py).

## Using the OpenDaylight SDN Controller with the Mininet

In this lab example, I will use two virtual machines. One will run the Mininet emulated network and the other will run the OpenDaylight controller. I will connect both VMs to a host-only network so they can communicate with each other and with programs running on the host computer, such as ssh and the X11 client.

I will use VirtualBox to run the Mininet VM that I downloaded from the mininet project web site, which is the easiest way to experiment with Mininet. The Mininet project team provides an Ubuntu 14.04 LTS VM image with Mininet 2.2.1, Wireshark and OpenFlow dissector tools already installed and ready to use.

My setup :

- Host : Ubuntu 18.04

- CPU : Intel i3 5005U

- RAM : 12 GB

- Hypervisor : VirtualBox 6

### Setting up the OpenDaylight Virtual Machine

To build the OpenDaylight virtual machine, I downloaded the Ubuntu 18.04 ISO image from the ubuntu.com web site. Then I installed it in a new VM in VirtualBox.

Give the virtual machine a descriptive name. I named the virtual machine OpenDaylight. Configure it so it uses two CPUs and 2 GB or RAM. This is the minimum configuration to support OpenDaylight. Then add a host-only network adapter to the VM.

![odl](odl.png)

In the VM’s VirtualBox network settings, enable two network interfaces. Connect the first network adapter to the NAT interface (which is the default setting) and the second network adapter to the host-only network, vboxnet0.

![odl_network](odl_network.png)

Note: If you don't have a host-only network enabled, click CTRL+H, this will lead you to the Host network manager, then create a new one and don't forget to enable the DHCP server.

![odl_network_host](odl_network_host.png)

List all the devices using th ip addr show command:

![odl_ip](odl_ip.png)

### Connect to the OpenDaylight VM using SSH

I like to use a terminal application when working on Virtual Machines. The VirtualBox console window has too many annoying limitations. For example, I cannot cut-and-paste text from my host system onto the VirtualBox console attached to the virtual machine, or vice-versa.

Open a terminal on host computer and login using SSH:

![odl_ssh](odl_ssh.png)

> **Optional** : To enable SSH auto login, I suggest you this [link](https://www.linuxbabe.com/linux-server/setup-passwordless-ssh-login)

Now you are connected to the OpenDaylight virtual machine and can see that the host name in the prompt is changed to is odl, which I configured when installing Ubuntu on the VM.

I also enabled X forwarding when I started SSH so I can run X programs on the OpenDaylight VM, although we won’t do that in this tutorial.

### Installing Java and OpenDayLight

In this lab, we're gonna use Nitrogen release (0.7.3) since l2switch was removed in Fluorine, so any version before that (Oxygen would be the most recent) should have l2switch. It was removed because the project no longer had an active community.

```bash
# Run an apt-get update to ensure that your server receives all of the most recent security and application packages.
$ sudo apt-get update
# Now, install the following convenience packages, to make life easier.
$ sudo apt-get -y install unzip vim wget
# Run the following command to install the JRE.
$ sudo apt-get -y install openjdk-8-jre
# Now, ensure that Ubuntu points to JAVA 8. Run the following command. If it does not point to JAVA 8, be sure to select version 8 from the list.
$ sudo update-alternatives --config java
# With the path in hand, run the following command to update your BASHRC file.
$ echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre' >> ~/.bashrc
# Now source your BASHRC file and then check to ensure $JAVA_HOME lives in the environment.
$ source ~/.bashrc
# Double check that $JAVA_HOME ends with /jre.
$ echo $JAVA_HOME
# Download the OpenDaylight Zip Archive using Wget
$ wget https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.7.3/karaf-0.7.3.zip
# Make a directory for the binary.
$ sudo mkdir /usr/local/karaf
# Move the zip archive to the install workspace
$ sudo mv karaf-0.7.3.zip /usr/local/karaf 
$ sudo unzip /usr/local/karaf/karaf-0.8.4.zip -d /usr/local/karaf/ #Unzipping
# Install karaf into user space.
$ sudo update-alternatives --install /usr/bin/karaf karaf /usr/local/karaf/karaf-0.8.4/bin/karaf 1
$ sudo update-alternatives --config karaf
# Execute the karaf command via sudo and pass the -E flag to keep the $JAVA_HOME environment variable.   
$ sudo -E karaf
```

![odl_karaf](odl_karaf.png)

> Java terminal error troubleshoot ([ERROR] Failed to construct terminal; falling back to unsupported
java.lang.NumberFormatException: For input string: "0x100") :  

```bash

$ export TERM=xterm-color
$ source /.bashrc

```

### Installing OpenDayLight features

Next, install the minimum set of features required to test OpenDaylight and the OpenDaylight GUI, type this command inside the karaf cli:

```bash
opendaylight-user@root> feature:install odl-restconf odl-l2switch-switch odl-mdsal-apidocs odl-dlux-core odl-dluxapps-nodes odl-dluxapps-topology odl-dluxapps-yangui odl-dluxapps-yangvisualizer odl-dluxapps-yangman
```

Once installed, these features are permanently added to the controller and will run every time it starts.

## Set up the Mininet Virtual Machine

Start the Mininet VM in the VirtualBox Manager. Now we should have two VMs running: OpenDaylight VM and Mininet VM. If we started the OpenDaylight VM first, it will have IP address 192.168.56.101 and the mininet VM will receive the second available IP address on the host-only network, 192,168.56.102. We can verify this by running the ip command on the Mininet VM console :

![mininet_ip](mininet_ip.png)

> Note: The Mininet VM is based on Ubuntu Server 14.04, which does not yet use the predictable network interface names like enp0s3 and enp0s8, so we see interface names like eth0 and eth1.

### Connect to the Mininet VM using SSH

Now open a terminal window on your host computer and SSH into the Mininet VM. Turn X forwarding on. (If you are using Windows, use Xming for an X Window System Server and Putty as an SSH client)

![mininet_ssh](mininet_ssh.png)

### Start Mininet

On the Mininet VM, start a simple network topology. In this case, we will do the following:

- Set up three switches in a linear topology

- Each switch will be connected to one host

- The MAC address on each host will be set to a simple number

- The remote controller, OpenDaylight, is at IP address 192.168.56.101:6633 (We will use OpenFlow version 1.3)

The Mininet command to start this is:

```bash
mininet@mininet-vm:~$ sudo mn --topo linear,3 --mac --controller=remote,ip=192.168.56.101,port=6633 --switch ovs,protocols=OpenFlow13
```

Then test it with *pingall* command.

![mininet_topo](mininet_topo.png)

### The OpenDaylight Graphical User Interface

Open a browser on your host system and enter the URL of the OpenDaylight User Interface (DLUX UI). It is running on the OpenDaylight VM so the IP address is 192.168.56.102 and the port, defined by the application, is 8181, So the URL is: http://192.168.56.101:8181/index.html 

The default username and password are both admin.

Now we see the network topology in the OpenDaylight controller’s topology tab.

![odl_topology](dlux.png)

You can see the network that is emulated by the Mininet network emulator. You may test OpenDaylight functionality by building different network topologies in Mininet with different attributes, and by using OpenDaylight to run experiments on the emulated network. For example, you may break links between switches in Mininet to test how the network responds to faults.

## Other Resources

[RFC 7426](https://tools.ietf.org/html/rfc7426)
