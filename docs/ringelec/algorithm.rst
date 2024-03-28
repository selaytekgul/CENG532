.. include:: substitutions.rst

|RINGELEC|
=========================================

Background and Related Work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This section delves into election algorithms for distributed systems, specifically focusing on ring topologies. Election algorithms allow processes within a network to designate a single leader responsible for coordinating tasks, maintaining data consistency, and facilitating communication.

Chang-Roberts Algorithm: This algorithm targets directed rings and leverages process IDs for leader selection. Messages with the highest ID propagate throughout the ring, ultimately identifying the leader process [ChangRoberts1979]_.
Franklin's Algorithm: Designed for undirected rings, this algorithm involves active processes comparing their IDs with neighboring processes in both directions. Processes with lower IDs become passive, while the process with the highest ID emerges as the leader [Franklin1982]_.
These algorithms offer distinct approaches to leader election in ring networks, with trade-offs in terms of message complexity and execution time.

Distributed Algorithm: Chang-Roberts |RINGELEC| 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Chang-Roberts  :ref:`Algorithm <ChangRobertsAlgorithm>` [ChangRoberts1979]_ , proposed by Chang and Roberts, aims to oﬀer a robust approach to leader election in directed ring networks, characterized by the following key strengths:

- Directed Rings: Works best in directed ring networks for optimized communication.

- ID-based Election: Uses process IDs (highest wins) for eﬃcient leader selection.

- Guaranteed Termination: Ensures the election concludes with a single leader.

- Scalable Messages: Message complexity scales proportionally with the network size.



.. _ChangRobertsAlgorithm:

.. code-block:: RST
    :linenos:
    :caption: Chang-Roberts algorithm.
    
    initialize:
        id = unique identifier for each process
        successor = process's successor in the ring
    
    send_message:
        send message with id to successor
    
    upon_message_receive(received_id):
        if received_id > id:
            become passive
            forward message
        else if received_id < id:
            discard message
        else:
            declare as leader
    
    detect_leader:
        if received own message:
            declare as leader


1. Each process has a unique identifier.
2. Each process sends a message with its identifier to its successor in the ring.
3. Upon receiving a message:
    a. If the received identifier is greater than its own, the process becomes passive and forwards the message.
    b. If the received identifier is less than its own, the process discards the message.
    c. If the received identifier is equal to its own, the process declares itself as the leader.
4. The process that initiated the election can detect its own message coming back to it, indicating it is the leader.

Example
~~~~~~~~

Application of the provided algorithm to a scenario involving three processes: A, B, and C.

**Initialization:**

Each process is assigned a unique identifier.
Process A's successor is B, Process B's successor is C, and Process C's successor is A.

**Sending Messages:**

1. Process A sends a message with its identifier to Process B.
2. Process B sends a message with its identifier to Process C.
3. Process C sends a message with its identifier to Process A.
4. Upon Receiving a Message:

**When Process B receives a message from A:**
Since the received identifier (A's identifier) is less than its own identifier (B's identifier), Process B discards the message.

**When Process C receives a message from B:**
Since the received identifier (B's identifier) is less than its own identifier (C's identifier), Process C discards the message.

**When Process A receives a message from C:**
Since the received identifier (C's identifier) is greater than its own identifier (A's identifier), Process A becomes passive and forwards the message.

**Detecting the Leader:**
Each process monitors the messages it sends.
When Process A detects its own message returning to it, it declares itself as the leader.
This example demonstrates the application of the algorithm with three processes (A, B, and C), where each process sends messages to its successor in the ring, evaluates received messages based on their identifiers, and ultimately identifies the leader based on the return of its own message.

Correctness
~~~~~~~~~~~

*Termination (liveness)*:
The algorithm ensures that the election concludes with a single leader within a finite number of steps. Here's why:

- Process Activity: Each process participates actively by sending its ID in a message.
- Bounded Message Flow: Messages propagate through the ring until reaching the process with the highest ID.
- Passive Behavior: Processes with lower IDs become passive upon receiving a higher ID, preventing them from sending further messages.
- Guaranteed Termination: Since only the process with the highest ID remains active, eventually it will receive its own message back, signifying it's the leader, and the election terminates.
    
*Correctness*:
The algorithm guarantees that the elected leader is indeed the process with the highest unique identifier within the ring network. Here's the reasoning:

- ID-based Selection: Processes compare their own IDs with the IDs received in messages.
- Passive High-ID Processes: Processes with higher IDs become passive upon receiving them, preventing them from further participation.
- Leader Determination: The process that receives its own message back is guaranteed to have the highest ID within the ring and becomes the leader.

Therefore, the Chang-Roberts algorithm ensures that the election concludes within a finite time (termination) and elects the correct process with the highest ID (correctness).

Complexity 
~~~~~~~~~~

    1. **Time Complexity:**  The Chang-Roberts :ref:`Algorithm <ChangRobertsAlgorithm>` has a time complexity of O(D), where D represents the diameter of the ring network. Here's the explanation:

- Message Propagation: The algorithm relies on message propagation, where an election message containing a process ID travels through the ring.
- Diameter Dependence: In the worst case scenario, the message might need to traverse the entire diameter (D) of the ring to reach the process with the highest ID.
- Finite Termination: Since message propagation is bounded by the network diameter, the algorithm guarantees termination within O(D) time units.
    2. **Message Complexity:** The Chang-Roberts :ref:`Algorithm <ChangRobertsAlgorithm>` has a message complexity of 2 \|E\|, where \|E\| denotes the number of processes (edges) within the ring network. Here's the breakdown:

- Message Sending: Each process actively participates by sending a single message containing its ID to both its neighbors.
- Total Messages: Since there are 2 neighbors for each process, the total number of messages sent becomes 2 \|E\|.


Distributed Algorithm: Franklin's |RINGELEC| 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

in  :ref:`Algorithm <FranklinsAlgorithmLabel>` designed for undirected ring topologies, offers an improvement over the message complexity of the Chang-Roberts algorithm. In each round of the election process, every active process compares its own ID with the IDs of its immediate active neighbors on both sides. The algorithm proceeds as follows:

- Initialization:

Each process in the ring has a unique identifier.
At the beginning of an election round, each active process sends its ID to its neighboring processes on both sides.
Comparing IDs:

When an active process, say p, receives messages tagged with IDs q and r from its neighbors, it evaluates the following cases:

- If max{q, r} < p's ID: p initiates another election round by sending its ID to both neighbors again.

- If max{q, r} > p's ID: p becomes passive.

- If max{q, r} = p's ID: p becomes the leader.

Handling Message Overtaking:

Since a message can overtake another from the previous round, processes need to keep track of the parity of their current round number and include this parity information in the message containing their ID.

.. _FranklinsAlgorithmLabel:

.. code-block:: RST
    :linenos:
    :caption: Franklin's algorithm.
    
    initialize:
        id = unique identifier for each process
        active = true
        leader = false
        round_number = 0
    
    send_message:
        send message with id to both neighbors
    
    upon_message_receive(received_id, parity):
        if active:
            if received_id > id:
                become passive
                forward message with received_id and parity
            else if received_id < id:
                discard message
            else:
                leader = true
                broadcast leader message
        else:
            if parity == round_number:
                become leader
    
    detect_leader:
        if leader message received:
            declare as leader

1. Initialization: Each process initializes its unique identifier, sets its state to active, and initializes the leader variable to false. Additionally, a round number variable is introduced to track the current round of the algorithm.

2. Sending Messages: Each active process sends a message containing its ID to both neighbors.

3. Upon Message Receive: When a process receives a message containing an ID and parity from a neighbor, it evaluates whether it remains active or becomes passive based on the comparison of received ID with its own. If it becomes passive, it forwards the message. If the received ID matches its own, it declares itself as the leader and broadcasts a leader message. If a process is passive and receives a message with a matching parity, it also declares itself as the leader.

4. Detecting the Leader: Each process monitors for leader messages. If a leader message is received, the process declares itself as the leader.


Example
~~~~~~~~

Franklin's algorithm using three processes: A, B, and C, in an undirected ring topology.

**Initialization:**

Each process is assigned a unique identifier. Let's say:

- Process A has ID = 3
- Process B has ID = 5
- Process C has ID = 7

All processes start in an active state.

**Round 1:**

- Process A sends its ID (3) to both neighbors (B and C).
- Process B sends its ID (5) to both neighbors (A and C).
- Process C sends its ID (7) to both neighbors (A and B).
Upon Message Receive:

Process A (ID = 3):

- Receives ID = 7 from C and ID = 5 from B.
- ID 7 is greater than 3, so A becomes passive and forwards ID = 7 to B.
- ID 5 is smaller than 3, so A discards the message from B.
Process B (ID = 5):

- Receives ID = 3 from A and ID = 7 from C.
- ID 3 is smaller than 5, so B discards the message from A.
- ID 7 is greater than 5, so B becomes passive and forwards ID = 7 to C.
Process C (ID = 7):

- Receives ID = 5 from B and ID = 3 from A.
- ID 5 is smaller than 7, so C discards the message from B.
- ID 3 is smaller than 7, so C discards the message from A.

**Round 2:**

Process A and B are now passive, so they do not send messages.
Process C is the only active process and sends its ID (7) to both neighbors (A and B).

**Upon Message Receive:**

Process A (ID = 3):

Receives ID = 7 from C.
A is passive, so it checks the parity of the round. Since the parity matches the round number (even), A declares itself as the leader.
Process B (ID = 5):

Receives ID = 7 from C.
B is passive and does not take any action.
Process C (ID = 7):

Receives ID = 7 from both A and B.
C is active but does not need to proceed as it has received its own ID from both neighbors.
Leader Detection:

Process A, upon receiving its own ID from C, declares itself as the leader.
Therefore, in this example, Process A is elected as the leader using Franklin's algorithm in an undirected ring topology with processes A, B, and C.

Correctness
~~~~~~~~~~~

*Termination (liveness)*:
Franklin's algorithm guarantees the election concludes with a single leader within a finite number of rounds with high probability. Here's the reasoning:

- Structured Rounds: The algorithm employs a fixed number of rounds for message exchange and state updates, ensuring progress towards a leader selection.
- Probabilistic Tie-Breaking: In each round, processes with the potential to be the leader participate in a probabilistic selection process. With each round, the probability of selecting a single leader increases.
- Bounded Rounds: Even in worst-case scenarios with a high number of processes with identical IDs, the number of rounds remains bounded, ensuring eventual termination.    
*Correctness*:
Franklin's algorithm strives to elect the process with the highest unique identifier within the ring network with high probability. Here's the explanation:

- ID Comparison: Processes compare their own IDs with the IDs received from neighbors during each round.
- Probabilistic Selection: In rounds where multiple processes might be potential leaders, the random selection mechanism helps break ties and favor processes with higher IDs.
- Convergence Towards Highest ID: As rounds progress, processes with lower IDs are more likely to be eliminated, increasing the chance of selecting the process with the highest ID.
- Therefore, while Franklin's algorithm introduces an element of randomness, it ensures termination within a bounded number of rounds and strives to elect the correct process with the highest ID with high probability.
Complexity 
~~~~~~~~~~

    1. **Time Complexity:**   Unlike Chang-Roberts, the Franklin's :ref:`Algorithm <FranklinsAlgorithmLabel>` doesn't have a definitive worst-case time complexity due to its probabilistic nature.

Here's why:

- Rounds and Communication: The algorithm employs a structured approach using rounds, where processes exchange messages and update their states in each round.
- Probabilistic Tie-Breaking: In scenarios with identical process IDs, a random selection element helps break ties and avoid deadlocks.
- Convergence: With each round, the probability of electing a leader increases. However, the exact number of rounds required cannot be guaranteed due to randomness.
    2. **Message Complexity:** The Franklin's :ref:`Algorithm <FranklinsAlgorithmLabel>`  message complexity is similar to Chang-Roberts and scales proportionally with the network size:

- Message Exchange: Processes exchange messages containing their state information during each round.
- Bounded Messages: The number of messages exchanged per round is limited by the number of neighbors (2) in a bidirectional ring.
- Total Messages: The total message complexity depends on the number of rounds, which is influenced by the probability of tie-breaking and the number of processes. In most cases, it is expected to be proportional to the number of edges (\|E\|).


.. [Fokking2013] Wan Fokkink, Distributed Algorithms An Intuitive Approach, The MIT Press Cambridge, Massachusetts London, England, 2013
.. [Tel2001] Gerard Tel, Introduction to Distributed Algorithms, CAMBRIDGE UNIVERSITY PRESS, 2001
.. [Lamport1985] Leslie Lamport, K. Mani Chandy: Distributed Snapshots: Determining Global States of a Distributed System. In: ACM Transactions on Computer Systems 3. Nr. 1, Februar 1985.
.. [ChangRoberts1979] Ernest Chang, Rosemary Roberts. An Improved Algorithm for Decentralized Extrema-Finding in Circular Configurations of Processes, ACM, 1979
.. [Franklin1982] Randolph Franklin. On an improved algorithm for decentralized extrema finding in circular configurations of processors. Commun. ACM, 1982
