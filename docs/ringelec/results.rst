.. include:: substitutions.rst

Implementation, Results and Discussion
======================================

Implementation and Methodology
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this section, the implementation details and methodologies employed for both the Chang and Roberts Algorithm and Franklin's Algorithm are explored.

**Chang and Roberts Algorithm:**

- Approach: Designed for rings where processes have unique identifiers. Messages with process IDs are circulated, and a process remains active if its own ID is larger than the IDs it receives. The process with the largest ID eventually becomes the leader.
*Advantages:*

- Efficiency Improvement: Notably enhances message complexity compared to basic flooding algorithms, contributing to more streamlined communication in ring networks.
- Straightforward Implementation: Relatively straightforward to implement due to its clear-cut logic and reliance on simple message circulation principles.
*Disadvantages:*

- Message Complexity: Despite being an improvement over basic flooding algorithms, it still exhibits a worst-case message complexity of O(n^2), which can become prohibitive for larger networks.
- Dependency on Unique Identifiers: The algorithm heavily relies on the existence of unique identifiers for each process, limiting its applicability in scenarios where such identifiers are not readily available.

**Franklin's Algorithm:**

- Approach: Designed for bidirectional rings. It uses the concept of "waves" of messages, where a process can start a wave if its ID is larger than its neighbors. Waves travel in both directions, and collisions resolve in favor of the larger ID. Eventually, the largest ID prevails.
*Advantages:*

- Optimized Message Complexity: Offers a significant improvement in terms of message complexity with a worst-case scenario of O(n log n), particularly beneficial for larger ring networks.
- Scalability: Due to its efficient message complexity, it scales well with increasing network size, making it suitable for a wide range of applications.
*Disadvantages:*

- Complex Implementation: Implementation of Franklin's algorithm can be considerably more complex compared to simpler algorithms like Chang and Roberts, requiring a deeper understanding of bidirectional message propagation and collision resolution.
- Communication Channel Requirements: Relies on bidirectional communication channels between neighboring processes, which may pose challenges in certain network architectures where such channels are not readily available or feasible.


Results
~~~~~~~~

Present your AHCv2 run results, plot figures.


This is probably the most variable part of any research paper, and depends upon the results and aims of the experiment. For quantitative research, it is a presentation of the numerical results and data, whereas for qualitative research it should be a broader discussion of trends, without going into too much detail. For research generating a lot of results, then it is better to include tables or graphs of the analyzed data and leave the raw data in the appendix, so that a researcher can follow up and check your calculations. A commentary is essential to linking the results together, rather than displaying isolated and unconnected charts, figures and findings. It can be quite difficulty to find a good balance between the results and the discussion section, because some findings, especially in a quantitative or descriptive experiment, will fall into a grey area. As long as you not repeat yourself to often, then there should be no major problem. It is best to try to find a middle course, where you give a general overview of the data and then expand upon it in the discussion - you should try to keep your own opinions and interpretations out of the results section, saving that for the discussion [Shuttleworth2016]_.


.. image:: figures/CDFInterferecePowerFromKthNode2.png
  :width: 400
  :alt: Impact of interference power


.. list-table:: Title
   :widths: 25 25 50
   :header-rows: 1

   * - Heading row 1, column 1
     - Heading row 1, column 2
     - Heading row 1, column 3
   * - Row 1, column 1
     -
     - Row 1, column 3
   * - Row 2, column 1
     - Row 2, column 2
     - Row 2, column 3

Discussion
~~~~~~~~~~

Present and discuss main learning points.




.. [Shuttleworth2016] M. Shuttleworth. (2016) Writing methodology. `Online <https://explorable.com/writing-methodology>`_.