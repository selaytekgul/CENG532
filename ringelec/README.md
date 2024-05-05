Distributed algorithms developed:
Ring Election: Chang-Roberts algorithm (Full)
Ring Election: Franklin's algorithm (Full)

# Chang-Roberts Algorithm

The Chang-Roberts Algorithm is a distributed algorithm used to elect a leader in a network of nodes arranged in a logical ring topology. In this algorithm, nodes communicate with each other by passing messages around the ring until a leader is elected. The algorithm is designed to work in asynchronous systems where nodes do not have access to global information about the network.

## Overview

The algorithm operates in rounds, with each node initially in an "active" state, meaning it participates in the election process. Nodes exchange messages containing their IDs, and based on these messages, nodes transition to a "passive" state if they encounter a node with a higher ID. The process continues until only one node remains in the "active" state, at which point it is elected as the leader.

## Components

### `State` Enum
Defines the possible states of a node: active, passive, or leader.

### `ChangRobertsMessageHeader`
Defines the message header for communication between nodes in the Chang-Roberts Algorithm.

### `ChangRobertsPayload`
Defines the payload for messages exchanged between nodes, containing the ID of the sending process.

### `ChangRobertsNode`
Represents a node in the system implementing the Chang-Roberts Algorithm. Each node has an ID and a state, and participates in the election process by sending and receiving messages.

## Usage

1. Instantiate nodes with unique IDs in the range [1, N], where N is the size of the ring.
2. Nodes exchange messages according to the algorithm rules until a leader is elected.
3. The node with the highest ID remaining in the "active" state after all message exchanges is elected as the leader.

# Franklins Algorithm

The Franklins Algorithm is another distributed algorithm used for leader election in a ring network of nodes. Similar to Chang-Roberts, nodes in the Franklins Algorithm communicate with each other by passing messages around the ring until a leader is elected. However, Franklins Algorithm differs in its message passing strategy.

## Overview

In Franklins Algorithm, each node sends messages to both of its neighbors in the ring, rather than just one neighbor as in Chang-Roberts Algorithm. This allows for redundancy in message passing and can potentially lead to faster convergence in the election process.

## Components

### `State` Enum
Defines the possible states of a node: active, passive, or leader.

### `FranklinsMessageHeader`
Defines the message header for communication between nodes in the Franklins Algorithm.

### `FranklinsPayload`
Defines the payload for messages exchanged between nodes, containing the ID of the sending process.

### `FranklinsNode`
Represents a node in the system implementing the Franklins Algorithm. Each node has an ID and a state, and participates in the election process by sending and receiving messages to both of its neighbors.

## Usage

1. Instantiate nodes with unique IDs in the range [1, N], where N is the size of the ring.
2. Nodes exchange messages according to the algorithm rules until a leader is elected.
3. The node with the highest ID remaining in the "active" state after all message exchanges is elected as the leader.
