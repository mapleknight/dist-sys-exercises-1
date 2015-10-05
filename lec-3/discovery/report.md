#Report for HW4 DiscoveryServer V1

##Team members

**protocol designer** : Sultan Alamro

**programmers** : Ke Wang, Zhenyang Tang, Xiaohua Sun, Sultan Alamro

##System Capability

This DiscoveryServer can be used to find the right conversion server that can serve the conversion between two specific units. 

##Protocol Specification

The protocol of DiscoveryServer supports three services : add, remove, lookup. DiscoveryServer communicates with clients using socket.

**1. Add conversion server to DiscoveryServer**

Conversion server sends : add <unit1> <unit2> <ip_address> <port_no>\n

DiscoveryServer response : success\n **OR** failure [reason]\n

**2. Remove conversion server from DiscoveryServer**

Conversion server sends : remove <ip_address> <port_no>\n

DiscoveryServer response : success\n **OR** failure [reason]\n

**3. Lookup a conversion service from DiscoveryServer**

Client sends : remove <unit1> <unit2>\n

DiscoveryServer response : <ip_address> <port_no>\n **OR** none **OR** failure [reason]\n

##Test Plan

### Compile and run DiscoveryServer.java

```
javac DiscoveryServer.java
java DiscoveryServer 5555
```

### Use "telnet" to test this server

**1. test "add" request**

Request :
```
telnet <server_ip> 5555
add kg lbs 10.0.0.10 5556
```

Response :
```
success
```

If we try to add another service which has same ip and port, the response will be :
```
failure exist
```

**2. test "lookup" request**

Request, look for a service that can serve the conversion between kg and lbs :
```
telnet <server_ip> 5555
lookup kg lbs
```

Response : 
```
10.0.0.10 5556
```

If we want to look for a service that has not been added to DiscoveryServer, the response will be :

Response : 
```
none
```

**3. test "remove" request**

Request, remove the service we have added in test case 1. :
```
telnet <server_ip> 5555
remove 10.0.0.10 5556
```

Response : 
```
success
```

If we want to remove this service again, the response will be :

Response : 
```
none
```

If we want to remove a service we have never added, the response will be :

Response : 
```
none
```


