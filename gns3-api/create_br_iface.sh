#! /bin/bash


sudo ip link add gns3 type bridge
sudo ip link set gns3 up
sudo ip addr add 192.168.77.254/24 dev gns3
