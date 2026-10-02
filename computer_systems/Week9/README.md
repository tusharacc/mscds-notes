# Week 9: Computer Networking Devices and Routing

## Overview
This week covers networking devices at different OSI layers, router architecture and operations, longest prefix matching algorithms, switching fabrics, and network domains (broadcast and collision domains).

---

## 1. Computer Networking Devices

### 1.1 Device Classification by Layer

Networking devices operate at different layers of the OSI model:

#### Layer 1 Devices (Physical Layer)
- **Repeaters and Hubs**: Operate in broadcast mode
  - Take input signal and send to all physical ports except input port
  - No concept of addresses
  - Work with electrical/optical signals

#### Layer 2 Devices (Data Link Layer)
- **Bridges and Switches**: Work with MAC addresses
  - Send frames to selected physical ports based on destination MAC address
  - Intelligent forwarding based on learned MAC addresses

#### Layer 3 Devices (Network Layer)
- **Routers**: Work with IP addresses
  - Send packets to selected physical ports based on destination IP address
  - Route traffic between different networks

#### Multi-Layer Devices
- **Gateways**: Can operate at any layer
  - Provide interoperability between networks
  - Contain protocol translators, impedance matchers, fault isolators, signal translators
  - Communicate using multiple protocols
  - Connect different types of networks

---

### 1.2 Repeaters

**Purpose**: Extend LAN range by amplifying signals

**Key Characteristics**:
- Layer 1 device working with electrical/optical signals
- Physical properties limit LAN length (signal degradation)
- Continuously monitor and amplify input signals
- Join LANs together

**Types**:
- **Local vs Remote Repeater**
- **Wired vs Wireless Repeater**: Used in homes/offices for extending connectivity
- **Digital vs Analog Repeater**: Based on signal type

---

### 1.3 Hubs

**Purpose**: Multi-port repeater for connecting multiple devices

**Key Characteristics**:
- Layer 1 device (no notion of addresses)
- Works in **half-duplex** mode
- Takes input signal, amplifies, and broadcasts to all ports except input port
- One collision domain for all connected devices

**Limitations**:
- Security risk: All devices receive all broadcasts
- Wasted bandwidth: Only one device can transmit at a time
- Collision domain includes all connected devices
- Overall throughput = Total bandwidth / Number of nodes

**Types**:
1. **Active Hub**:
   - Has own power supply
   - Can clean, boost, and relay signals
   - Serves as repeater and wiring center

2. **Passive Hub**:
   - Collects wiring/power from active hub
   - Simply relays signals without cleaning or boosting
   - Limited functionality due to limited power supply

**Summary of Repeaters and Hubs**:
- Make network seem like one large shared link
- Each bit sent everywhere
- Limited overall throughput
- Cannot support multiple technologies
- No concept of buffer or interpret rates

---

### 1.4 Bridges

**Purpose**: Segment LANs intelligently at Layer 2

**Key Characteristics**:
- Layer 2 devices working with MAC addresses
- Learn MAC addresses over time
- Segment LANs so each can carry its own traffic
- Usually has two ports (can have multiple)
- Creates multiple collision domains

**Operation**:
- Intelligently forward traffic between LANs based on destination MAC address
- Don't forward traffic unnecessarily
- Each side of bridge forms separate collision domain

**Example**: With two LANs connected via bridge:
- Two collision domains (one per LAN)
- Traffic isolation between segments

---

### 1.5 Switches

**Purpose**: Multi-port bridges with enhanced capabilities

**Key Characteristics**:
- Layer 2 devices (like bridges)
- Treated as combination of hub and bridge
- Support **full-duplex** communication (if links support it)
- Each port forms its own collision domain
- Saves bandwidth through selective forwarding

**Full-Duplex vs Half-Duplex**:
- **Half-duplex**: Single coaxial cable, one direction at a time
- **Full-duplex**: Twisted pair cables (2 for input, 2 for output), simultaneous bidirectional communication

**MAC Address Learning (Self-Learning)**:

Initial state: Empty MAC address table with columns:
- MAC Address
- Port Number

**Learning Process Example**:
1. PC-A (MAC: AAAA) sends frame to PC-C (MAC: CCCC)
2. Switch receives frame, learns: AAAA is on Port 1
3. Switch doesn't know C's location, broadcasts to all ports
4. PC-C receives and may respond
5. Switch learns: CCCC is on Port 3
6. Future frames forwarded only to specific ports

**Benefits**:
- **Traffic isolation**: Frames forwarded only to necessary segments
- **Separate transmissions**: Each segment operates independently
- Bandwidth savings compared to hubs
- Security: Information only delivered to destination host

---

## 2. Router Fundamentals

### 2.1 Router Basics

**Definition**: Layer 3 device that routes traffic between different networks

**Port Configuration**:
- Fewer WAN ports (typically one for ISP connection)
  - Usually colored blue
- Multiple LAN ports for internal network
  - Usually colored yellow

**Typical Home Network Setup**:
```
H1, H2, H3... (Hosts) → Router (with built-in switch) → ISP
```

---

### 2.2 Basic Router Operation

**Packet Processing Steps**:
1. **Receive packet** from inside or outside network
2. **Extract header information**
3. **Look up forwarding table** to determine output interface
4. **Update header** if required:
   - Decrease Time To Live (TTL)
   - Update checksum
5. **Queue packet** for transmission to appropriate output interface

**Forwarding Table**: Maps destination address to outgoing interface

---

### 2.3 Router Design Considerations

Two key design factors:

#### 1. Lookup Table Placement
- **Centralized table** (Control plane):
  - Would create contention bottleneck
  - All line cards accessing same table
- **Distributed tables** (Data plane):
  - **Solution**: Each line card maintains own copy of forwarding table
  - Enables local, fast decision making

#### 2. Line Card Interconnection
- **Shared bus**:
  - Only one can speak at a time
  - Requires CSMA/CD protocol
  - Inefficient for high-speed operation
- **Switching fabric** (Crossbar switch):
  - **Solution**: Non-competing input-output pairs communicate simultaneously
  - Enables parallel transmissions

---

### 2.4 Control Plane vs Data Plane

**Control Plane**:
- Decision-making component (the "brain")
- Sets routing rules and policies

**Data Plane**:
- Carries and forwards data (the "hands")
- Executes forwarding decisions based on control plane rules

---

## 3. Lookup Algorithms

### 3.1 MAC Address Lookup (Layer 2)

**Characteristics**:
- 48-bit address
- Device-specific identifier
- Manufacturer-specific bits + Device-specific bits
- Devices from different manufacturers have different formats

**Lookup Method**:
- **Exact match** required
- Common technique: **Hashing**
  - Hash MAC address to find output port
  - Fast O(1) lookup time

**Why exact match?**
- Unlike IP addresses, MAC addresses don't follow hierarchical structure
- Devices in same network may come from different manufacturers
- No common subnet mask concept

---

### 3.2 IP Address Lookup (Layer 3)

**Characteristics**:
- 32-bit address (IPv4)
- Hierarchical organization
- Network ID + Host ID structure
- Devices in same network share network prefix

**Lookup Method**:
- **Longest Prefix Match (LPM)**
- Find most specific route possible
- More specific = fewer hosts in that network

**Network Structure**:
```
IP Address: [Network ID | Host ID]
            [   NID     |  HID   ]
```

Example: `/24` network
- First 24 bits: Network ID (same for all devices)
- Last 8 bits: Host ID (unique per device)

**Routing Logic**:
- Routers look for network ID matches
- Try to find most specific match (longest prefix)
- More specific route = fewer hosts = better routing decision

---

## 4. Longest Prefix Match (LPM)

### 4.1 LPM Concept

**Goal**: Find longest address prefix that matches destination address

**Principle**:
- Exact match is ideal but not always possible
- Use longest matching prefix to find most specific route
- More bits matched = more specific route = fewer hosts in that network

---

### 4.2 LPM Examples

#### Example 1: Basic LPM
```
Given IP: 10010000.10100000.00001010.00011111

Routing Table:
10010000.10100000.0*       → Port A (16 bits match)
10010000.10100000.00001*   → Port B (21 bits match)
10010000.10100000.00001010.* → Port C (24 bits match)

Result: Port C (longest match - 24 bits)
```

**Process**:
1. Compare IP with each table entry bit by bit
2. Continue matching until mismatch occurs
3. Select entry with longest match
4. More specific route chosen (fewer hosts possible)

#### Example 2: Comparison
```
Given IP: 192.168.20.191

Prefix Table:
192.168.20.0/24   → More specific (24 bits)
192.168.0.0/16    → Less specific (16 bits)

Result: 192.168.20.0/24 (longest prefix match)
```

Convert to binary for verification:
- Both match on first 16 bits (192.168)
- First entry matches additional 8 bits (20)
- Total match: 24 bits vs 16 bits
- Choose /24 route

#### Example 3: Complex Match
```
Given IP: 68.211.6.120

Prefix Table:
68.211.0.0/16
68.211.6.0/24
68.211.7.0/24
68.211.6.128/25

Process (in binary):
1. First octet matches: 01000100 (68)
2. Second octet matches: 11010011 (211)
3. Third octet varies:
   - Entry 1: Ends at /16
   - Entry 2: 00000110 (6) - matches!
   - Entry 3: 00000111 (7) - no match
   - Entry 4: 00000110.1 (6.128+) - no match (IP is .120 < 128)

Result: 68.211.6.0/24 (output port determined by longest match)
```

---

## 5. LPM Implementation

### 5.1 Software Implementation: Binary Trie

**Definition**:
- **Binary**: Each node has maximum 2 child nodes
- **Trie**: Prefix tree/search tree encoding routing table

**Structure**:
- Root node with two children: 0 and 1
- Each level represents one bit position
- Leaf nodes or intermediate nodes store output port information

**Example Routing Table**:
```
Prefix          Port
0*              A
10*             B
101*            C
```

**Corresponding Trie**:
```
        Root
       /    \
      0      1
     [A]     |
             0
            [B]
             \
              1
             [C]
```

**Lookup Process**:

Example 1: Input `1011`
1. Start at root
2. Read bit 1 → go right
3. Read bit 0 → go left to node B
4. Read bit 1 → go right to node C
5. Read bit 1 → no further nodes
6. Terminate at C → Output: Port C

Example 2: Input `1000`
1. Start at root → 1 → 0 → 0
2. At third 0: Node exists but no child for next 0
3. Backtrack to parent node B
4. Output: Port B

**Phone Book Analogy**:
- Similar data structure used for phone contact search
- Press keys (2=ABC, 3=DEF, etc.)
- Trie matches based on number sequence
- Quick match as you type

**Performance**:
- **Lookup time**: O(n) where n = max bits to search
- For IPv4: Maximum 32 nodes to traverse
- Very fast for typical prefixes
- Worst case: /32 prefix requires all 32 nodes

**Limitations**:
- Long prefixes (/30, /32) require many node traversals
- Can be improved with multi-bit tries

---

### 5.2 Multi-bit Trie Optimization

**Concept**: Each edge represents multiple bits instead of single bit

**Benefits**:
- Reduces tree depth
- Fewer node traversals
- Faster lookup for long prefixes

**Example**:
```
Single-bit:  111* → Root → 1 → 1 → 1 → Port A

Multi-bit:   111* → Root → 11 → {10, 11} → Port A
```

**Wildcard Handling**:
- `111*` where `*` is don't care
- In 2-bit representation: Both `1110` and `1111` map to same port
- Multiple nodes represent same output port

---

### 5.3 Hardware Implementation: TCAM

**CAM (Content Addressable Memory)**:
- Hash-like lookup structure
- Takes tag/address as input → produces value as output
- **Exact match** in O(1) time
- Used for fast hardware lookups

**TCAM (Ternary Content Addressable Memory)**:
- Extension of CAM for router implementation
- **Three matching states**: 0, 1, and X (don't care)
- Enables prefix matching in hardware

**Matching Example**:
```
Stored word: 10XX0
Matches:     10000, 10010, 10100, 10110
```

---

### 5.4 TCAM LPM Implementation

**Routing Table to TCAM Conversion**:

```
Prefix        TCAM Format      Priority
0/0     →     XXXX            Lowest  (least specific)
10/2    →     10XX            Medium
111/3   →     111X            High
101/3   →     101X            High    (most specific)
```

**Critical Rule**: **Sort by prefix length (most specific first)**

**Priority Order** (top to bottom):
1. 101X (3-bit prefix - most specific)
2. 111X (3-bit prefix - most specific)
3. 10XX (2-bit prefix)
4. XXXX (0-bit prefix - default route)

**Lookup Process Example**:

Search word: `1011`

**Parallel matching** (all circuits activated simultaneously):
```
Position 0: 1 matches 1,1,1,X ✓
Position 1: 0 matches 0,1,0,X → 111X fails, continue with 101X, 10XX, XXXX
Position 2: 1 matches 1,X,X   → continue with 101X, 10XX, XXXX
Position 3: 1 matches X,X,X   → continue with 101X, 10XX, XXXX

Matches: 101X, 10XX, XXXX (3 matches)
```

**Result**: Select **topmost** match → 101X (output port 00)

**TCAM Advantages**:
- **Parallel processing**: All comparisons happen simultaneously
- **O(1) lookup time**: Constant time regardless of table size
- **Hardware speed**: Much faster than software tries
- **Simple priority**: Topmost match wins

---

## 6. Switching Fabrics

### 6.1 Router Architecture

**Line Card Design**:
- Each line card maintains **own copy** of forwarding table
- Avoids centralized table bottleneck
- Enables parallel, independent decision making
- Data plane operates autonomously based on control plane rules

**Interconnection Options**:

#### Shared Bus (Poor choice)
- Only one line card can transmit at a time
- Requires CSMA/CD protocol
- Bottleneck for high-speed routers
- Inefficient bandwidth utilization

#### Crossbar Switch (Preferred)
- Non-competing input-output pairs can communicate simultaneously
- Enables parallel transmissions
- Much higher throughput
- Efficient bandwidth utilization

---

### 6.2 Crossbar Switching

**Structure**: Grid of connections between input and output ports

```
Input Ports    Crossbar Grid    Output Ports
1  ────────────┬──┬──┬───────── 1
2  ────────────┼──┼──┼───────── 2
3  ────────────┼──┼──┼───────── 3
4  ────────────┼──┼──┼───────── 4
5  ────────────┼──┼──┼───────── 5
6  ────────────┴──┴──┴───────── 6
```

**Operation**:
- Activate only non-competing channels
- Multiple simultaneous transmissions possible

**Example Simultaneous Transmissions**:
- Input 1 → Output 4 ✓
- Input 2 → Output 6 ✓
- Input 3 → Output 5 ✓

All can operate in same time slot (no competition)

**Invalid Scenario**:
- Input 1 → Output 4
- Input 2 → Output 4 ✗ (both want output 4 - conflict!)

---

### 6.3 Head-of-Line (HOL) Blocking

**Problem**: Packet at front of queue blocks packets behind it, even when their destinations are available

#### Example 1: Simple HOL Blocking
```
Input 1: [R] [R] [R] → All want Red output
Input 2: [R] [G] [B] → Red, Green, Blue
Input 3: [R] [R] [K] → Red, Red, Black

Scenario:
- Input 1's first packet gets Red output
- Input 2's first packet blocked (Red busy)
- Input 3's first packet blocked (Red busy)
- Green, Blue, Black outputs are FREE but blocked!
```

**Result**: Green, Blue, and Black packets cannot proceed even though their output ports are available

#### Example 2: Complex HOL Blocking
```
Input 1: [4] [3] [2] [1]
Input 2: [2] ...
Input 3: [4] [3] ...
Input 4: [1] ...

Active connections:
- Input 2 → Output 2 ✓ (active)
- Input 4 → Output 1 ✓ (active)
- Input 1 wants Output 4
- Input 3 wants Output 4
- Conflict! One gets through, one blocked

If Input 1 → Output 4:
- Input 3 blocked (wants 4)
- Output 3 is FREE but Input 1's second packet [3] cannot proceed

If Input 3 → Output 4:
- Input 1 blocked (wants 4)
- Output 3 is FREE but Input 1's second packet [3] cannot proceed
```

**Key Issue**: Packets behind blocked head packet cannot proceed even when their destinations are available

---

### 6.4 Solution: Virtual Output Queues (VOQ)

**Concept**: Instead of single queue per input, maintain N queues (one per output)

**Traditional Single Queue**:
```
Input 1: [Pkt→Out3] [Pkt→Out1] [Pkt→Out2]
         └─ If blocked, all behind it wait
```

**Virtual Output Queues**:
```
Input 1:
  Queue for Output 1: [Pkt] [Pkt]
  Queue for Output 2: [Pkt]
  Queue for Output 3: [Pkt] [Pkt] [Pkt]
```

**Benefits**:
- If Output 3 busy, packets for Output 1 and 2 can still proceed
- No HOL blocking between different output destinations
- Better bandwidth utilization
- Higher throughput

**Operation**:
- Incoming packet sorted into appropriate virtual queue based on destination
- Each virtual queue managed independently
- Scheduler selects from non-blocked queues

---

## 7. Broadcast and Collision Domains

### 7.1 Definitions

**Broadcast Domain**:
- Collection of hosts that a broadcast frame can reach
- Area where broadcast by one host reaches all other hosts
- Defines scope of Layer 2 broadcasts

**Collision Domain**:
- Section of network where packet collision occurs if two nodes transmit simultaneously
- Area where simultaneous transmissions interfere with each other
- Relevant in half-duplex communications

---

### 7.2 Hubs: Broadcast and Collision Domains

**Hub Behavior**:
- Receives packet on one port
- Broadcasts to all other ports (except input port)
- Every host receives every transmission

**Domains**:
- **Broadcast Domain**: 1 (all connected hosts)
- **Collision Domain**: 1 (all connected hosts)

**Implications**:
- Any broadcast reaches all hosts
- Only one host can transmit at a time
- If two hosts transmit simultaneously → collision
- Collision affects all hosts on the hub
- Limited scalability and performance

---

### 7.3 Switches: Broadcast and Collision Domains

**Switch Behavior**:
- Forwards based on MAC address (learned over time)
- Sends unicast frames only to destination port
- Broadcasts only when:
  - Destination MAC unknown
  - Destination MAC is FF:FF:FF:FF:FF:FF (broadcast)

**Layer 2 Broadcast**:
- Destination MAC: FF:FF:FF:FF:FF:FF (48 bits all set to 1)
- Switch must forward to all ports
- Reaches every host in LAN

**Domains** (for switch with 4 connected hosts):
- **Broadcast Domain**: 1 (all connected hosts)
- **Collision Domain**: 4 (one per port)

**Why 4 Collision Domains?**
- Each switch port = separate collision domain
- Port-specific communication
- In half-duplex: Collision only between switch and connected host on that port
- Other ports unaffected by collisions on different ports

**Formula**:
```
Broadcast Domains = 1
Collision Domains = Number of connected ports
```

---

### 7.4 Full-Duplex vs Half-Duplex Impact

#### Half-Duplex Links
- Single shared medium (e.g., coaxial cable)
- Only one direction at a time
- Collision possible if both sides transmit
- Each port is separate collision domain
- Still need CSMA/CD protocol

#### Full-Duplex Links
- Separate transmit and receive paths
- RJ45 twisted pair: 4 pairs, 2 for RX, 2 for TX
- Both sides can transmit simultaneously
- **No collisions possible**
- CSMA/CD can be disabled

**Modern Reality**:
- Most modern networks use full-duplex
- Collision domain concept less relevant
- Still matters when:
  - Switch connected to hub (becomes half-duplex)
  - Defective network cards causing interference
  - Legacy equipment in network

**Summary**:
- Switch = collision domain separator
- Each switch interface = separate collision domain

---

### 7.5 Routers: Broadcast and Collision Domains

**Router Behavior**:
- Separates both broadcast and collision domains
- Broadcast from one network doesn't cross to another network
- Creates network boundaries

#### Broadcast Types

**1. Local Broadcast (Limited Broadcast)**:
```
Destination IP: 255.255.255.255
```
- Reaches all hosts in local network
- Router **drops** these packets (doesn't forward)
- Router may respond but won't cross network boundaries

**2. Directed Broadcast Address (DBA)**:
```
Format: Network ID with all Host ID bits set to 1

Example for 192.168.1.0/24:
DBA = 192.168.1.255
```

**DBA Behavior**:

Scenario: Network N1 (with Router R1) → Router R2 → Network N2 (192.168.1.0/24)

- Host in N1 sends packet to 192.168.1.255
- R1 doesn't recognize it as DBA (unaware of N2's subnet mask)
- R1 may forward as regular IP
- **R2 recognizes it as DBA for N2**
- **R2 drops the packet** (security risk to allow external DBA)

**Key Point**:
- Having 255 in last octet ≠ always broadcast
- Could be valid host IP (e.g., 10.0.0.255/16 is valid host)
- Context (subnet mask) determines if it's DBA

**Summary**:
- Local broadcast: Doesn't cross router
- DBA: Receiving router drops it for security
- Routers break both broadcast and collision domains

---

### 7.6 Domain Counting Example

**Network Topology**:
```
        [Switch]                    [Switch]
        /  |  \                     /  |  \
       PC  PC  PC                  PC PC  PC
        \  |  /                     \  |  /
         [Router]
```

**Collision Domains** (count each link):
- Left switch: 3 collision domains (3 PC ports)
- Right switch: 3 collision domains (3 PC ports)
- Total: **6 collision domains**

**Broadcast Domains** (separated by router):
- Left side of router: 1 broadcast domain
- Right side of router: 1 broadcast domain
- Total: **2 broadcast domains**

---

### 7.7 Modern Network Considerations

#### Wired Networks
- Use switches to reduce/eliminate collisions
- **Half-duplex links**: Each switch port = own collision domain
- **Full-duplex links**: Collision possibility eliminated
- Hubs/repeaters in network → still consider collision domains
- Gigabit Ethernet and faster:
  - No hubs/repeaters exist
  - All devices full-duplex
  - Can **ignore collision domain** concept

#### Wireless Networks (WiFi)
- Operate on shared medium (radio frequencies)
- Same frequency transmissions → collisions
- **Still need collision domain consideration**
- CSMA/CA protocol used
- Collision detection more complex than wired

**Conclusion**: Collision domains still relevant in:
- Legacy networks with hubs
- Half-duplex links
- Wireless networks
- Networks with potentially defective hardware

---

## Summary

### Key Concepts Covered

1. **Networking Devices**:
   - Layer 1: Repeaters, Hubs (broadcast, no intelligence)
   - Layer 2: Bridges, Switches (MAC-based, learning capability)
   - Layer 3: Routers (IP-based, inter-network routing)
   - Multi-layer: Gateways (protocol translation, interoperability)

2. **Router Architecture**:
   - Control plane vs Data plane
   - Distributed forwarding tables (per line card)
   - Crossbar switching for parallel transmissions

3. **Lookup Algorithms**:
   - MAC: Exact match using hashing
   - IP: Longest Prefix Match (LPM)
   - Software: Binary tries (O(n) lookup)
   - Hardware: TCAM (O(1) lookup)

4. **Switching Challenges**:
   - Head-of-Line blocking problem
   - Solution: Virtual Output Queues

5. **Network Domains**:
   - Broadcast domains (scope of broadcasts)
   - Collision domains (scope of collisions)
   - Device-specific behavior (hub vs switch vs router)
   - Modern considerations (full-duplex, wireless)

### Important Takeaways

- **Switches** improve upon hubs by creating separate collision domains per port
- **Routers** separate both broadcast and collision domains
- **LPM** is fundamental to IP routing (most specific route wins)
- **TCAM** provides hardware-accelerated LPM in modern routers
- **Crossbar switching** enables parallel packet forwarding
- **Virtual output queues** solve head-of-line blocking
- **Full-duplex** modern networks largely eliminate collision concerns in wired networks
- **Wireless networks** still require collision domain management
