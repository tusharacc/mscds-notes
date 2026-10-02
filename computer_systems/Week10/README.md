# Week 10: Middleboxes and Network Address Translation (NAT)

## Overview
Week 10 explores the practical implementation of the internet through middleboxes - intermediary devices that break the simple network model but solve real-world networking challenges. The focus is on understanding various types of middleboxes, with deep coverage of Network Address Translation (NAT) and its variants.

---

## Table of Contents
1. [Introduction to Middleboxes](#introduction-to-middleboxes)
2. [Firewalls](#firewalls)
3. [Load Balancers](#load-balancers)
4. [WAN Accelerators](#wan-accelerators)
5. [Tunneling and VPN](#tunneling-and-vpn)
6. [Network Address Translation (NAT)](#network-address-translation-nat)
7. [Static NAT and PAT](#static-nat-and-pat)
8. [Dynamic NAT and PAT](#dynamic-nat-and-pat)
9. [Policy NAT and Twice NAT](#policy-nat-and-twice-nat)

---

## Introduction to Middleboxes

### Ideal vs. Practical Internet

**Ideal Internet Design:**
- Every device has a unique and fixed IP address (globally unique identifier)
- All devices are reachable from everywhere
- Network nodes simply forward packets without modification or filtering

**Practical Internet Challenges:**
- **Host Mobility**: Devices switch networks while stationary or moving
  - Example: Switching between WiFi bands (2.5 GHz to 5 GHz)
  - Physical movement between network ranges
- **Address Depletion**: IPv4 provides ~4 billion addresses (2^32)
  - Global population: ~7 billion
  - Average devices per person: 5+ (phone, laptop, TV, smart home devices, etc.)
  - Total devices >> available IPv4 addresses
- **Security Concerns**: Need for traffic filtering and protection
- **Performance Issues**: Load balancing for replicated services
- **Incremental Deployment**: Mixed technology deployments over time

### What are Middleboxes?

**Definition**: Intermediary devices interposed between communicating hosts, usually transparent to end users.

**Key Characteristics:**
- Break the simple network model
- Violate the concept of layering
- Can cause network problems
- Are a practical necessity for solving real problems
- Not likely to disappear from networks

**Common Types:**
- Address translators
- Firewalls
- Traffic shapers
- Intrusion detection systems
- Transparent proxies
- Application accelerators

---

## Firewalls

### Purpose
Act as filters to keep dangerous packets out of the network and prevent malicious activities.

### Inspection Mechanisms

**Packet-by-Packet Filtering** examining:
1. **Header Information:**
   - Source and destination IP addresses
   - Port numbers
   - Protocol type (e.g., TCP, UDP)
2. **Connection State:**
   - TCP SYN packets (SYN=1, ACK=0) for connection initiation
   - TCP flags and handshake status
3. **Message Types**
4. **Deep Packet Inspection (DPI)**: Examining packet content (if unencrypted)

### Example Filtering Rules

**Block UDP and Telnet:**
```
Block: IP Protocol Field 17 (UDP)
Block: Source/Destination Port 23 (Telnet)
```

**Block External Connection Attempts:**
```
Block: Incoming TCP packets with SYN=1 and ACK=0
Allow: Outbound connections from internal clients
```

### Rule Ordering Example

**Scenario:**
- Alice's Network: 222.22.0.0/16
- Bob's Network: 111.11.0.0/16
- Trudy's Subnet (untrusted): 111.11.11.0/24
- Alice's Accessible Subnet: 222.22.22.0/24

**Requirements:**
1. Allow Bob's hosts to connect to Alice's specific subnet (222.22.22.0/24)
2. Block Trudy's subnet (111.11.11.0/24) completely
3. Block all other internet traffic

**Correct Rule Order (Option D):**
1. **First**: Deny 111.11.11.0/24 → 222.22.0.0/16 (Block Trudy)
2. **Second**: Allow 111.11.0.0/16 → 222.22.22.0/24 (Allow Bob)
3. **Third**: Deny all other traffic

**Why Order Matters:**
- Rules are evaluated sequentially
- First match determines packet fate
- Incorrect order can block intended traffic or allow unwanted traffic

### Firewall Types

#### Stateless Firewalls
- Treat every packet independently
- No memory of previous packets
- Examine each packet regardless of flow
- Simple but less efficient

#### Stateful Firewalls
- Remember connection-level information
- Track connection state
- Allow return traffic based on established connections
- More intelligent filtering
- Example: If outbound connection allowed, corresponding inbound response is automatically allowed

---

## Load Balancers

### Purpose
Distribute traffic across multiple servers to optimize resource utilization and prevent overload.

### Architecture

```
Client Requests → Load Balancer (Common IP) → Server 1 (IP1)
                                            → Server 2 (IP2)
                                            → Server 3 (IP3)
```

### Benefits

1. **Traffic Distribution**: Balances load across all servers
2. **Single Entry Point**: All requests come to one common IP address
3. **Fault Tolerance**: If one server fails, others can take over
4. **Scalability**: Easy to add/remove servers

### Failover Mechanism

**Server Failure Handling:**
- Failed server: 10.0.0.1
- Replacement server: 10.0.0.3
- Replacement sends **Gratuitous ARP**: "10.0.0.1 has MAC address [10.0.0.3's MAC]"
- Load balancer continues sending requests to 10.0.0.1 (handled by replacement)

**Connection Impact:**
- **New Connections**: Can be handled normally
- **Existing Connections**: May drop (replacement server unaware of previous state)

---

## WAN Accelerators

### Purpose
Also called WAN optimizers or bandwidth accelerators, these provide common services to all hosts on a network.

### Services Provided

1. **Compression/Decompression**
2. **Buffering**
3. **Caching**
4. **TCP Optimization**

### Architecture

```
Office 1 Computers → WAN Appliance 1 → Internet → WAN Appliance 2 → Office 2 Server
```

### Use Cases

#### 1. Compression
- Appliance compresses uncompressed files from clients
- Opposite appliance decompresses for destination
- No client-side upgrade needed
- Transparent to end systems

#### 2. TCP Throughput Optimization
- Appliance buffers TCP segments with large local memory
- Responds quickly to sender (simulating large window)
- Actual delivery to client happens as client is ready
- Overcomes client's limited buffer capacity

#### 3. Caching
- Store frequently requested content locally
- Serve subsequent requests from cache (if fresh)
- Reduces latency and bandwidth usage
- Faster response for repeated queries

**Benefits:**
- No need to upgrade every computer
- Centralized service provision
- Transparent operation to end users
- Cost-effective performance improvement

---

## Tunneling and VPN

### Tunneling Concept

**Purpose**: Create a virtual point-to-point link between two nodes, hiding the actual endpoints.

### How Tunneling Works

**Without Tunneling:**
```
Packet: [Encrypted Data | Source: 1.1.1.10 | Dest: 2.2.2.10]
```
- Anyone intercepting sees 1.1.1.10 ↔ 2.2.2.10 are communicating

**With Tunneling (Encapsulation):**
```
Outer Packet: [Inner Packet | Source: 1.1.1.1 (tunnel device) | Dest: 2.2.2.1 (tunnel device)]
Inner Packet: [Encrypted Data | Source: 1.1.1.10 | Dest: 2.2.2.10]
```
- Interceptor sees only 1.1.1.1 ↔ 2.2.2.1 communication
- Actual endpoints (1.1.1.10 and 2.2.2.10) are hidden
- Multiple host pairs can use the same tunnel

### VPN (Virtual Private Network)

**Architecture:**
```
Client (1.2.3.4) → VPN Server (proxy) → Destination (3.4.5.6)
```

**Characteristics:**
- Communication through a proxy server
- Bypasses censorship and network restrictions
- Hides actual source from destination
- Requires full trust in VPN service provider

**Risks:**
- VPN provider can intercept requests
- Potential for fake responses
- Malicious activity if provider is untrustworthy

---

## Network Address Translation (NAT)

### The Problem

**Address Depletion:**
- Organization started with small IP range
- Business growth requires more addresses
- Problems:
  1. No more IP addresses available from ISP
  2. Available ranges non-contiguous (fragmented)
  3. Every machine doesn't need public IP

**Solution:**
- Internal hosts use private IP addresses
- Few public IP addresses shared for external communication
- NAT maps private ↔ public addresses

### NAT Terminology

**Device Types:**
- Router (common NAT device)
- Firewalls
- Load balancers

**Port Categories:**
- **Port 0**: Special port for local programs (not used for network traffic)
- **Well-known Ports (1-1023)**: Require superuser privilege to bind
- **Registered Ports (1024-49151)**: No superuser privilege needed
- **Private/Dynamic/Ephemeral Ports (49152-65535)**: Temporary services

### NAT vs PAT

| Feature | NAT (Network Address Translation) | PAT (Port Address Translation) |
|---------|-----------------------------------|-------------------------------|
| **Modifies** | Layer 3 (IP) headers only | IP + Port (Layer 3 + 4) |
| **Translation** | IP → IP | (IP, Port) → (IP, Port) |
| **Example** | 10.1.1.11 → 73.8.2.11 | (10.1.1.11, 3333) → (73.8.2.11, 7777) |

### Static vs Dynamic Translation

| Feature | Static | Dynamic |
|---------|--------|---------|
| **Post-translation** | Explicitly defined by admin | Selected by device at runtime |
| **Mapping** | Permanent (one-to-one) | Temporary (one-to-many or many-to-one) |
| **Use Case** | Hosting servers | Home routers, client connections |

### Translation Direction

**Outbound Packets:**
- Source IP/Port is translated

**Inbound Packets:**
- Destination IP/Port is translated

---

## Static NAT and PAT

### Static NAT

**Definition**: Post-translation IP address is explicitly defined and permanently mapped.

**Characteristics:**
- One-to-one IP mapping
- Permanent translation
- Bidirectional (works both directions)

**Use Case**: Hosting a server on private IP network

**Example:**
```
Internal Server: 10.2.2.33 (private, non-routable)
Public IP: 73.8.2.33 (routable)
Static mapping: 10.2.2.33 ↔ 73.8.2.33
```

**Traffic Flow:**

*Outbound (Server to Internet):*
```
Before NAT: [Data | Src: 10.2.2.33 | Dest: x.x.x.x]
After NAT:  [Data | Src: 73.8.2.33 | Dest: x.x.x.x]
```

*Inbound (Internet to Server):*
```
Before NAT: [Data | Src: x.x.x.x | Dest: 73.8.2.33]
After NAT:  [Data | Src: x.x.x.x | Dest: 10.2.2.33]
```

**Key Observations:**
- Outbound: Source is translated
- Inbound: Destination is translated
- Bidirectional: No prerequisite for connection direction

### Static PAT

**Definition**: Static translation of (IP, Port) pair to another (IP, Port) pair.

#### Use Case 1: Multiple Services on Different Servers

**Scenario**: Host multiple services with one public IP

```
Public IP: 73.8.2.44

HTTP Server:  10.4.4.41:8080
HTTPS Server: 10.4.4.42:443

Mappings:
73.8.2.44:80  → 10.4.4.41:8080 (HTTP)
73.8.2.44:443 → 10.4.4.42:443 (HTTPS)
```

**How It Works:**
- Client accesses http://site.com (port 80)
- NAT translates: 73.8.2.44:80 → 10.4.4.41:8080
- Client accesses https://site.com (port 443)
- NAT translates: 73.8.2.44:443 → 10.4.4.42:443

**Return Traffic:**
- Source and destination swap
- Same translation rules apply in reverse

#### Use Case 2: Non-Standard Ports

**Problem**: Hosting service on non-standard port (e.g., HTTP on 8080)

**Without Static PAT:**
- Clients must specify: www.mysite.com:8080
- Inconvenient and non-standard

**With Static PAT:**
```
External: 73.8.2.44:80
Internal: 10.4.4.41:8080

Mapping: 73.8.2.44:80 → 10.4.4.41:8080
```

- Clients access: www.mysite.com (default port 80)
- Automatically translated to internal port 8080

#### Use Case 3: Security Through Obscurity (Port Punching)

**SSH Security Example:**

**Standard Setup (Vulnerable):**
- SSH on port 22
- Attackers scan for open port 22
- Known attack vectors against SSH

**Secured Setup:**
```
External: 73.8.2.44:1234
Internal: 10.4.4.41:22

Mapping: 73.8.2.44:1234 → 10.4.4.41:22
```

**Benefits:**
- Only port 1234 responds externally
- Port 22 scans return nothing
- Secret port known only to authorized users
- Selective port opening (punch holes through firewall)

**Generalization:**
- Only specific external ports are forwarded
- Unlisted ports get no response
- Enhanced security through selective exposure

---

## Dynamic NAT and PAT

### Dynamic PAT

**Definition**: Post-translation (IP, Port) pair selected by router at runtime.

**Most Common Use**: Home WiFi routers

**Scenario:**
```
Public IP: 32.8.2.66 (single IP from ISP)
Internal Network: 10.6.6.0/24 (multiple devices)
```

#### How It Works

**Multiple Clients, One Public IP:**

| Internal Device | Internal IP:Port | Public IP:Port | Destination |
|----------------|------------------|----------------|-------------|
| Host A | 10.6.6.71:5555 | 32.8.2.66:7777 | Server X |
| Host B | 10.6.6.72:3333 | 32.8.2.66:8888 | Server Y |
| Host C | 10.6.6.73:3333 | 32.8.2.66:9999 | Server Y |

**Key Points:**
- Same public IP for all hosts
- Different port numbers ensure uniqueness
- Translation table tracks mappings

#### Source Port Randomization

**Why Randomize?**

**Problem Without Randomization:**
- Host B: 10.6.6.72:3333 → 32.8.2.66:3333
- Host C: 10.6.6.73:3333 → 32.8.2.66:3333
- **Collision**: Both map to identical (IP, Port) pair
- Return traffic cannot be distinguished

**Solution:**
- Randomize source port for all connections
- Creates unique (IP, Port) combinations
- Eliminates collision checking overhead

**Implementation:**
```
Host B: 10.6.6.72:3333 → 32.8.2.66:8888 (randomized)
Host C: 10.6.6.73:3333 → 32.8.2.66:9999 (randomized)
```

#### Directionality

**Unidirectional Characteristic:**
- **Outbound**: Connection initiated from inside creates table entry
- **Inbound**: Response allowed only if table entry exists
- **External Initiation**: Dropped if no existing entry

**Example:**
```
Host D (external) → 32.8.2.66:443
No table entry for port 443 → Packet dropped
(Even if internal HTTPS server exists on port 443)
```

**Implication**: Internal services not accessible from outside without prior outbound connection

### Dynamic NAT

**Definition**: Post-translation IP address selected by router at runtime (ports unchanged).

**Purpose**: Create temporary static NAT - assign temporary dedicated public IP to internal hosts.

#### Example Setup

```
Internal Network: 10.7.7.0/24
Available Public IPs: 54.5.4.1, 54.5.4.2, 54.5.4.3

Rule: Dynamic NAT internal network to public IP pool
```

#### How It Works

**IP Assignment:**

| Internal Host | Private IP | Assigned Public IP | Port |
|--------------|------------|-------------------|------|
| Host A | 10.7.7.71 | 54.5.4.1 | unchanged |
| Host B | 10.7.7.72 | 54.5.4.2 | unchanged |
| Host C | 10.7.7.73 | 54.5.4.3 | unchanged |
| Host D | 10.7.7.74 | **None** (dropped) | - |

**Key Characteristics:**
- Only IP addresses translated (ports unchanged)
- Limited by number of available public IPs
- Packets dropped when pool exhausted
- IPs reassigned when released

**IP Recycling:**
1. Host A finishes communication
2. 54.5.4.1 becomes available
3. Host D can now use 54.5.4.1

#### Directionality

**Conditionally Bidirectional:**
- **While IP Assigned**: Bidirectional communication possible
- **When IP Released**: Becomes unidirectional again
- Differs from Dynamic PAT (always unidirectional for external initiation)

#### Use Case: FTP Protocol

**FTP Requirements:**
- **Control Channel**: Client random port N → Server port 21
- **Data Channel**: Server port 20 → Client port M (specified during control)

**Problem with Dynamic PAT:**
```
Original rule: (Internal IP, Port N) → (Public IP, Port X)
Data channel: Server:20 → Public IP:M
No translation rule for port M → Dropped
```

**Solution with Dynamic NAT:**
```
Internal IP → Public IP (ports unchanged)
Control: Public IP:N → Server:21 ✓
Data:    Server:20 → Public IP:M ✓ (same IP, any port works)
```

#### Advantages vs Disadvantages

**Advantages:**
- Supports protocols requiring multiple connections on different ports
- Provides unique IP per host (while assigned)
- Moving target defense (IP changes over time)

**Disadvantages:**
- **No IP Conservation**: Equal public and private IPs needed for full coverage
- **Momentary Connectivity**: IP availability not guaranteed
- **One-to-One Mapping**: When all IPs assigned, new hosts blocked

**Alternative:**
- Configure multiple Static NAT rules for guaranteed unique mapping

---

## Policy NAT and Twice NAT

### Previous NAT Limitations

**Common Characteristics of All Four NAT Types:**
1. **Matching**: Done on ONE field (only source or only source IP:Port)
2. **Translation**: Done on ONE field (only source or only destination)

**Question**: What if we need to:
- Match on BOTH source AND destination?
- Translate BOTH source AND destination?

### Policy NAT

**Definition**: Match on BOTH source AND destination fields to make translation decision.

**Types**: Can be any of the four NAT types (Static/Dynamic NAT/PAT) + policy matching

#### Use Case: Conditional Translation Based on Destination

**Scenario**: Treat different destinations differently

**Configuration Example (Policy Dynamic PAT):**

```
Internal Network: 10.8.8.0/24
Public IP 1: 32.8.2.77
Public IP 2: 32.8.2.66

Rules:
1. IF (Source: 10.8.8.0/24) AND (Dest: 45.4.9.x)
   THEN Dynamic PAT to 32.8.2.77

2. IF (Source: 10.8.8.0/24) AND (Dest: ANY other)
   THEN Dynamic PAT to 32.8.2.66
```

**How It Works:**
- **Destination: 45.4.9.x** → Use public IP 32.8.2.77
- **Destination: All others** → Use public IP 32.8.2.66

**Key Point:**
- **Matching**: Source AND Destination (two fields)
- **Translation**: Source only (one field)
- Different public IPs for different destination categories

### Twice NAT

**Definition**: Perform NAT on BOTH source AND destination (translate twice).

**Formula**: Policy + Twice NAT
- **Policy**: Match on both source and destination
- **Twice**: Translate both source and destination

#### Use Case: DNS Server Redirection

**Scenario**: Redirect Google DNS queries to local DNS server

**Problem:**
- Organization computers default to Google DNS (8.8.8.8)
- Want to use local DNS server instead
- Impractical to reconfigure every computer

**Solution: Policy Twice NAT**

**Configuration:**
```
Internal Network: 10.9.9.0/24
Google DNS: 8.8.8.8:53
Local DNS: 32.9.1.88:53
Public IP for source: 32.8.2.55
```

**Rules:**
```
IF (Source: 10.9.9.0/24) AND (Dest: 8.8.8.8:53)
THEN:
  - Translate Source: 10.9.9.x → 32.8.2.55 (Dynamic PAT)
  - Translate Dest: 8.8.8.8:53 → 32.9.1.88:53 (Static NAT)
```

#### Traffic Flow Example

**Original Request:**
```
Source: 10.9.9.5:random
Dest:   8.8.8.8:53 (Google DNS)
```

**After Twice NAT:**
```
Source: 32.8.2.55:5555 (Dynamic PAT - randomized port)
Dest:   32.9.1.88:53   (Static NAT - local DNS)
```

**Process:**
1. **Matching**:
   - Source in 10.9.9.0/24 ✓
   - Destination is 8.8.8.8:53 ✓
2. **Translation**:
   - Source: Dynamic PAT (IP change + port randomization)
   - Destination: Static NAT (redirect to local DNS)

**Benefits:**
- No client configuration changes needed
- Transparent redirection
- Centralized DNS control
- Works for entire network

### Summary Table

| NAT Type | Match On | Translate | Directionality |
|----------|----------|-----------|----------------|
| **Static NAT** | Source | Source/Dest IP | Bidirectional |
| **Static PAT** | Source | Source/Dest IP:Port | Bidirectional |
| **Dynamic NAT** | Source | Source/Dest IP | Conditional Bidirectional |
| **Dynamic PAT** | Source | Source/Dest IP:Port | Unidirectional |
| **Policy NAT** | Source + Dest | Source/Dest | Depends on base type |
| **Twice NAT** | Source + Dest | Source + Dest | Depends on base type |

---

## Key Concepts Summary

### Middleboxes
- Necessary evil in modern networking
- Solve practical problems despite violating layering principles
- Include firewalls, load balancers, NAT devices, VPN servers, WAN accelerators

### Firewalls
- Packet filtering based on headers and state
- Rule order is critical
- Stateful vs stateless operation
- Protection against malicious traffic

### Load Balancers
- Distribute traffic across multiple servers
- Provide fault tolerance and scalability
- Single entry point for clients
- Handle server failures gracefully

### WAN Accelerators
- Provide compression, caching, buffering
- Transparent to end systems
- Improve performance without client upgrades
- Cost-effective optimization

### NAT
- Solves IPv4 address depletion
- Four basic types: Static/Dynamic × NAT/PAT
- Advanced: Policy NAT and Twice NAT
- Trade-offs between flexibility and complexity

### Design Considerations
- Security vs accessibility
- Performance vs resource usage
- Scalability vs simplicity
- Transparency vs control

---

## Important Distinctions

### NAT Terminology
- **NAT (narrow)**: IP-only translation
- **PAT**: IP + Port translation
- **NAT (broad)**: General term encompassing both NAT and PAT

### Translation Attributes
- **Pre-translation**: Always explicitly defined
- **Post-translation**:
  - Static: Explicitly defined
  - Dynamic: Selected at runtime

### Directionality
- **Bidirectional**: Static NAT, Static PAT
- **Conditional Bidirectional**: Dynamic NAT (while IP assigned)
- **Unidirectional**: Dynamic PAT (requires internal initiation)

### Matching vs Translation
- **Traditional NAT**: Match 1 field, Translate 1 field
- **Policy NAT**: Match 2 fields, Translate 1 field
- **Twice NAT**: Match 2 fields, Translate 2 fields

---

## Practical Applications

1. **Home Networks**: Dynamic PAT for sharing single ISP IP
2. **Enterprise Servers**: Static NAT/PAT for public services
3. **Security**: Port punching, firewall rules
4. **Performance**: Load balancing, WAN acceleration
5. **Privacy**: VPN tunneling
6. **Service Redirection**: Policy/Twice NAT for DNS, proxies
7. **Legacy Protocol Support**: Dynamic NAT for FTP

---

## Conclusion

Week 10 provides comprehensive coverage of how the internet works in practice, focusing on middleboxes as essential components despite their violation of ideal network principles. The detailed exploration of NAT variants demonstrates how practical networking requirements drive technical solutions, balancing security, performance, scalability, and resource constraints.
