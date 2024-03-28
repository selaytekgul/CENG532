.. include:: substitutions.rst
========
Abstract
========

This paper investigates two algorithms for leader election in ring networks: the Chang-Roberts algorithm and Franklin's algorithm. The purpose of the study is to compare and evaluate their effectiveness in selecting a leader within a distributed system. The Chang-Roberts algorithm employs a directed ring topology and prioritizes communication efficiency through ID-based election and guaranteed termination. In contrast, Franklin's algorithm operates in an undirected ring and aims to improve message complexity. Through simulation and analysis, it is found that both algorithms effectively elect a leader, with Chang-Roberts excelling in directed ring networks and Franklin's algorithm offering improved scalability in terms of message complexity. These findings provide valuable insights into selecting the appropriate leader election algorithm based on network topology and resource constraints within distributed systems.