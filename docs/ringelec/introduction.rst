.. include:: substitutions.rst

Introduction
============
    
Distributed systems, where tasks are divided and executed across numerous computer processes, often require a designated coordinator process to ensure smooth operation. This coordinator plays a vital role in managing tasks, maintaining data consistency, and facilitating communication between processes. In specific network topologies, like rings where processes are connected in a closed loop, electing a leader becomes particularly crucial.

In the absence of a designated leader within a ring network, several challenges can arise:

- Uncoordinated Tasks: Processes might end up working on redundant tasks or waiting for instructions, hindering overall efficiency.
- Data Inconsistencies: The lack of a central point for data consistency management can lead to inconsistencies, where different processes possess different versions of the same data, causing errors and unexpected behavior.
- Inefficient Communication: In a leaderless ring, communication can become cumbersome. Processes might need to send messages through multiple hops in the ring to reach their destination, increasing communication overhead and latency.
These challenges motivate the investigation of leader election algorithms in ring topologies. Such algorithms allow processes to elect a single coordinator responsible for managing tasks, ensuring data consistency, and streamlining communication within the distributed system.

This research investigates the performance of two established ring election algorithms: Chang-Roberts and Franklin's. The analysis focuses on their efficiency in terms of message exchange and execution time required to elect a leader process within a ring topology.

- Chang-Roberts Algorithm: This algorithm targets a directed ring and leverages process IDs for leader selection. Messages with the highest ID propagate throughout the ring, ultimately identifying the leader process.

- Franklin's Algorithm: Designed for undirected rings, this algorithm involves active processes comparing their IDs with neighboring processes in both directions. Processes with lower IDs become passive, while the process with the highest ID emerges as the leader.

By evaluating these algorithms, the research aims to identify their strengths and weaknesses, providing valuable insights for selecting appropriate leader election protocols in ring-based distributed systems.

This research contributes to the field of distributed systems by:

- Implementation of both the Chang-Roberts Algorithm and the Franklin's Algorithm on the AHCv2 platform. The implementation specifics are detailed in Section 1.4.
- Providing a detailed analysis of Chang-Roberts and Franklin's algorithms in the context of ring topologies in Section 1.3.
- Comparing their performance through message exchange and execution time evaluation 1.4.2.
- Discussing the trade-offs between each algorithm's communication approach, message complexity, and suitability for various scenarios in the Sections 1.3.5 and 1.3.9.
- This research provides guidance for future endeavors in selecting efficient leader election algorithms for distributed systems with ring topologies.