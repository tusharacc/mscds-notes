# Week 8: Computer Networks and Internet Fundamentals

## Table of Contents
1. [Origins of the Internet](#origins-of-the-internet)
2. [Key Networking Concepts](#key-networking-concepts)
3. [Protocol Layering and Abstraction](#protocol-layering-and-abstraction)
4. [Naming and Addressing](#naming-and-addressing)
5. [Network Configuration](#network-configuration)
6. [How the Internet Works](#how-the-internet-works)

---

## Origins of the Internet

### ARPANET and Early Networking

The Internet evolved from **ARPANET** (Advanced Research Projects Agency Network), which was:
- The first wide-area packet-switched network with distributed control
- One of the first networks to implement the TCP/IP protocol suite
- A network connecting research institutions like Harvard, MIT, Utah, Xerox, and SRI

### Interface Message Processor (IMP)

**IMP** was a crucial early networking device:
- A packet switching node used to interconnect networks to ARPANET (late 1960s to 1989)
- The first generation of what we now call **routers**
- Required connection to a host computer via bit serial interface
- Essentially functioned as a **gateway** between networks

### Gateways vs Routers

**Gateways**:
- Provide interoperability between networks
- Contain devices such as protocol translators, impedance matchers, rate converters, fault isolators, and signal translators
- Communicate using more than one protocol to connect multiple networks
- Can operate on any of the seven layers of the OSI model
- Distinct from modern routers, which have integrated many networking functions

### What is the Internet?

The Internet is:
- A **publicly accessible network of interconnected computer networks**
- A network that uses **packet switching** to transmit data
- Based on standard **Internet protocols** (TCP/IP)
- A **best-effort packet delivery service** (no guaranteed delivery)
- A network where **power is at the edge** (processing occurs at endpoints)
- **Programmable** - new network services can be added at any time by anyone

---

## Key Networking Concepts

### 1. Abstraction Through Protocol Layering

**Why Layering?**
- Makes replacing individual layers easier without affecting others
- Separates concerns and manages complexity
- Each layer relies on services from layers below and provides services to layers above
- The interface between layers defines interaction while hiding implementation details

**Key Principles:**
- Layers are independent and replaceable
- Clear boundaries between layers
- Standardized interfaces

### 2. The Hourglass Model

The Internet protocol suite uses an **hourglass model**:

```
    Application Layer
    (HTTP, FTP, TFTP, etc.)
           |
    Transport Layer
    (TCP, UDP)
           |
      IP Layer      <- Thin network layer (narrow waist)
           |
    Network Access
    (Ethernet, etc.)
```

The **thin network layer (IP)** facilitates interoperability among different types of networks.

### 3. OSI vs TCP/IP Models

**OSI Model (7 Layers):**
1. Application Layer
2. Presentation Layer
3. Session Layer
4. Transport Layer
5. Network Layer
6. Data Link Layer
7. Physical Layer

**TCP/IP Model (4 Layers):**
1. **Application Layer** (combines OSI layers 5-7)
2. **Transport Layer** (same as OSI)
3. **Internet Layer** (same as OSI Network Layer)
4. **Network Access Layer** (combines OSI layers 1-2)

### 4. Protocol Data Units (PDUs)

Different names at different layers:

| Layer | OSI Name | TCP/IP Name |
|-------|----------|-------------|
| Application | Data/Message | Data/Message |
| Transport | Segment (TCP) / Datagram (UDP) | Segment/Datagram |
| Network/Internet | Packet | Packet |
| Data Link | Frame | Frame |
| Physical | Bit/Symbol | - |

### 5. Encapsulation Process

When sending data:
1. Application creates a **message**
2. Transport layer adds headers (creates **segment/datagram**)
3. Network layer adds headers (creates **packet**)
4. Data link layer adds headers (creates **frame**)

When receiving data, each layer strips its corresponding header and passes data up.

### 6. Resource Allocation

Networks must divide scarce resources among competing parties:
- Memory
- Link bandwidth
- Spectrum
- Paths
- Processing power

---

## Protocol Layering and Abstraction

### HTTP Example

**Application Layer Perspective:**
- Application only cares about making requests and receiving responses
- Example HTTP GET request:
```
GET /path/to/resource HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0
[CRLF]
```

**HTTP Response:**
```
HTTP/1.1 200 OK
Date: [timestamp]
Server: Apache
Last-Modified: [timestamp]
Content-Length: 23
[CRLF]
[Content]
```

The application doesn't need to know how the request/response travels across the network.

### Layer Communication

- Each layer communicates with its **corresponding layer** on the remote host
- HTTP talks to HTTP
- TCP talks to TCP
- IP talks to IP
- Ethernet talks to Ethernet (or other network access protocol)

### Layer Independence

Layers can be replaced independently:
- Ethernet can be replaced with SONET (Synchronous Optical Networking) or other technologies
- Upper layers continue to work without modification
- Only the interface needs to remain consistent

---

## Naming and Addressing

### 1. Socket and Process Communication

**Sockets** provide the interface between the OS and its networking subsystem.

**Components:**
- **IP Address**: Identifies the host (e.g., 1.2.3.4)
  - IPv4: 32-bit address
- **Port Number**: Identifies the process/application (16-bit number)
  - Example: Port 80 for HTTP
  - Port range: 0-65535

**Communication Example:**
- Client (IP: X, Port: R) → Server (IP: Y, Port: 80)
- Server response: (IP: Y, Port: 80) → Client (IP: X, Port: R)

**Port Types:**
- **Well-known ports**: 0-1023 (e.g., 80 for HTTP, 443 for HTTPS)
- **Registered ports**: 1024-49151
- **Dynamic/Private ports**: 49152-65535 (used by clients)

### 2. Uniform Resource Identifier (URI)

**URI** is a unique sequence of characters that identifies logical or physical resources.

**Generic Syntax:**
```
scheme://[user:password@]host[:port]/path[?query][#fragment]
```

**Components:**
- **Scheme**: Protocol (http, https, ftp, etc.)
- **Authority**:
  - Host name or IP address
  - Optional port number
  - Optional user info
- **Path**: Location on the host (case-sensitive)
- **Query**: Optional parameters
- **Fragment**: Optional reference to part of resource

### 3. URN vs URL

**URN (Uniform Resource Name):**
- Provides only a unique name
- Does NOT provide location information
- Example: ISBN of a book (identifies but doesn't locate)

**URL (Uniform Resource Locator):**
- Type of URI that provides both name AND location
- Tells you how to find and retrieve the resource
- Example: `https://en.wikipedia.org/wiki/Networking`

### 4. Domain Names

**Components of a URL:**
```
https://subdomain.example.com/directory/file.html
        |         |      |
    subdomain    SLD    TLD
```

- **TLD (Top-Level Domain)**: .com, .org, .edu, .net, etc.
- **SLD (Second-Level Domain)**: The main domain name
- **Subdomain**: Logical organization within a domain

**Domain Name Types:**

**Apex/Root/Bare Domain:**
- Does not include subdomain
- Example: `wikipedia.org`

**Subdomain:**
- Used to logically organize or separate sections of a website
- Can be a directory on the server
- Can also point to a different host
- Example: `en.wikipedia.org`, `mail.example.com`

**Hostname:**
- A domain name mapped to a host with an IP address
- Can be: `example.com` or `subdomain.example.com`
- Must have an associated IP address

**Key Relationships:**
- A hostname can be a domain name if properly organized in DNS
- A domain name can be a hostname if assigned to an internet host
- Subdomains can be directories OR separate hosts

### 5. Fully Qualified Domain Name (FQDN)

**FQDN** specifies the complete domain including the TLD.

**Example:**
- Hostnames: `Saturn`, `Jupiter`
- Domain: `pc`
- SLD: `net`
- FQDN: `Saturn.pc.net`, `Jupiter.pc.net`

Another example:
```
pc15.cs.ucla.edu
 |   |   |    |
host sub SLD  TLD
```

**Properties:**
- Can be a host or a subdomain
- Completely specifies location in DNS hierarchy

### 6. DNS (Domain Name System)

**DNS** serves as a "phone book" for the Internet:
- Translates human-friendly hostnames into IP addresses
- Hierarchical structure

**DNS Hierarchy:**
```
Root (.)
  |
  +-- TLD (.com, .org, .edu, .net)
       |
       +-- Second Level Domain (abc.com, ucla.edu)
            |
            +-- Subdomain (www, cs.ucla.edu, mail.ucla.edu)
                 |
                 +-- Host (pc15.cs.ucla.edu)
```

**How DNS Works:**
- When you type a domain name, your system queries the DNS server
- DNS server returns the corresponding IP address
- Responses are cached to improve performance

---

## Network Configuration

### 1. DHCP (Dynamic Host Configuration Protocol)

**DHCP** dynamically assigns IP addresses and network configuration to clients.

**Information Provided by DHCP:**
- **IP Address**: Unique identifier for the host
- **Subnet Mask**: Defines the network portion of the address
- **Default Gateway**: Router to use for non-local traffic
- **DNS Server Address**: Where to resolve domain names
- Other configuration parameters

**Benefits:**
- Automatic configuration
- Centralized management
- Prevents IP address conflicts
- Temporary leases allow address reuse

**Modern Routers:**
- Handle DHCP services
- Also perform routing, switching, NAT, firewall functions
- Single device with multiple capabilities

### 2. APIPA (Automatic Private IP Addressing)

**When DHCP Fails:**
- Host cannot get an IP from DHCP server
- Manual configuration is prevented or not available
- System needs to self-assign an address

**Link-Local Addresses:**
- Range: `169.254.0.0/16` (169.254.0.0 - 169.254.255.255)
- Total addresses: 65,536 (2^16)
- **Non-routable** - cannot communicate with external networks

**Conflict Detection with ARP:**
1. Host selects an IP from the link-local range (e.g., 169.254.1.1)
2. Sends ARP request: "Who has 169.254.1.1?"
3. If no response → IP is unique, can use it
4. If response received → someone else has that IP, choose another

### 3. ARP (Address Resolution Protocol)

**Purpose:** Resolve IP addresses to MAC addresses

**How ARP Works:**

1. **ARP Request** (broadcast):
   - "Who has IP address 192.168.1.1?"
   - Sent to all devices on local network (broadcast MAC: FF:FF:FF:FF:FF:FF)

2. **ARP Response** (unicast):
   - "MAC address XX:XX:XX:XX:XX:XX has 192.168.1.1"
   - Only the device with that IP responds

**ARP Table/Cache:**
- Stores IP-to-MAC mappings
- Reduces need for repeated ARP requests
- Entries have a timeout period

**Why Both IP and MAC?**
- **Layer 3 (IP)**: End-to-end addressing across networks
- **Layer 2 (MAC)**: Hop-to-hop addressing on local network
- Different purposes at different layers
- IP addresses are logical and routable
- MAC addresses are physical and local to each network segment

---

## How the Internet Works

### Complete Communication Flow Example

**Scenario:** Opening `http://www.iis.se` in a browser

**Initial Configuration:**
- Computer IP: 192.168.1.5
- Router LAN IP: 192.168.1.1
- Router WAN IP: 115.20.97.114
- DNS Server: 8.8.4.4
- Web Server: www.iis.se
- System is fresh (no cache)

### Step-by-Step Process

#### Step 1: Browser Request
- User types: `http://www.iis.se`
- Browser requests OS to establish connection to port 80

#### Step 2: DNS Resolution Needed
- OS needs IP address for `www.iis.se`
- Checks DNS cache → **empty**
- Must query DNS server

#### Step 3: DNS Query Preparation
Computer prepares DNS query:
- Source MAC: [Computer MAC]
- Source IP: 192.168.1.5
- Destination IP: 192.168.1.1 (DNS server)
- Destination Port: 53 (DNS)
- Source Port: [Random]
- Protocol: UDP
- **Missing**: Destination MAC address

#### Step 4: ARP Request (First)
Since MAC address is unknown:
1. OS puts DNS query in memory
2. Sends ARP request (broadcast):
   - "Who has 192.168.1.1?"
3. Router responds:
   - "MAC address [Router LAN MAC] has 192.168.1.1"
4. OS saves to ARP table
5. Now can complete DNS query

#### Step 5: DNS Query to Router
- DNS query sent to router with complete information
- Router receives query

#### Step 6: Router Processes DNS Query
Router checks:
- DNS cache → **empty**
- Must forward to DNS server (8.8.4.4)

Router creates new DNS query:
- Source MAC: [Router WAN MAC]
- Source IP: 115.20.97.114 (Router WAN IP)
- Destination IP: 8.8.4.4
- Destination MAC: [Next hop MAC]
- Source Port: [Random - different from client]
- Destination Port: 53

#### Step 7: DNS Resolution
- Query reaches DNS server
- DNS server resolves: `www.iis.se` → 143.75.19.3
- Response sent back

#### Step 8: DNS Response Path
**To Router:**
- Source IP: 8.8.4.4
- Destination IP: 115.20.97.114
- Content: `www.iis.se = 143.75.19.3`
- Router caches the result

**To Client:**
- Router forwards response
- Source IP: 192.168.1.1
- Destination IP: 192.168.1.5
- Client receives and caches the IP address

#### Step 9: TCP Three-Way Handshake

**SYN (Client → Server):**
- Source IP: 192.168.1.5
- Destination IP: 143.75.19.3
- Source Port: [Random, e.g., 1476]
- Destination Port: 80
- Source MAC: [Computer MAC]
- Destination MAC: [Router LAN MAC]

**NAT at Router:**
- Router performs **Network Address Translation**
- Changes source IP: 192.168.1.5 → 115.20.97.114
- Changes source MAC to WAN MAC
- Maintains port mapping for return traffic

**SYN-ACK (Server → Client):**
- Server responds with SYN-ACK
- Reaches router with destination 115.20.97.114
- Router does reverse NAT: 115.20.97.114 → 192.168.1.5
- Forwards to client

**ACK (Client → Server):**
- Client sends ACK
- Similar process through router
- Connection established

#### Step 10: HTTP Communication
Once TCP connection is established:
- Client sends: `GET / HTTP/1.1`
- Server responds with web page content
- All traffic goes through NAT translation at router

### Key Processes Involved

1. **DNS Resolution**: Domain name → IP address
2. **ARP Resolution**: IP address → MAC address (local network)
3. **NAT (Network Address Translation)**: Private IP ↔ Public IP
4. **TCP Three-Way Handshake**: Connection establishment
5. **HTTP Request/Response**: Application layer communication

### Important Observations

**Layer-Specific Addressing:**
- **Layer 2 (Data Link)**: Hop-to-hop using MAC addresses
- **Layer 3 (Network)**: End-to-end using IP addresses
- MAC addresses change at each hop
- IP addresses remain constant (except at NAT)

**Caching Benefits:**
- DNS cache: Avoid repeated DNS lookups
- ARP cache: Avoid repeated ARP requests
- Improves performance significantly

**NAT Translation:**
- Allows multiple devices to share one public IP
- Maintains connection state
- Translates private IPs to public IP for outbound traffic
- Reverses translation for inbound responses

**Best-Effort Delivery:**
- No guarantee of packet delivery
- Packets may be lost, delayed, or arrive out of order
- Higher-layer protocols (TCP) handle reliability
- Retransmissions and acknowledgments ensure data integrity

---

## Summary

Week 8 covered fundamental concepts of computer networking and how the Internet works:

1. **Historical Context**: Evolution from ARPANET using IMPs (early routers) to modern Internet infrastructure

2. **Architectural Principles**:
   - Protocol layering for abstraction and modularity
   - Hourglass model with IP as the thin waist
   - Power at the edge with programmable endpoints

3. **Addressing and Naming**:
   - Multiple addressing schemes (IP, MAC, ports)
   - URI/URL/URN for resource identification
   - DNS for name resolution
   - FQDN for complete host specification

4. **Network Configuration**:
   - DHCP for automatic configuration
   - APIPA for fallback addressing
   - ARP for MAC address resolution

5. **End-to-End Communication**:
   - Complete flow from browser to web server
   - Multiple protocols working together (DNS, ARP, TCP, HTTP)
   - NAT translation at network boundaries
   - Caching mechanisms for efficiency

The Internet is a complex system built on simple, layered principles that allow for scalability, flexibility, and interoperability across diverse networks worldwide.
