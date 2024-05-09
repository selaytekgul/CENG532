from enum import Enum
from random import randint

from adhoccomputing.Experimentation.Topology import Topology
from adhoccomputing.GenericModel import GenericModel, GenericMessageHeader, GenericMessagePayload, GenericMessage
from adhoccomputing.Generics import *

class State(Enum):
    """
    State of the nodes, one from {active, passive, leader}
    - "active" nodes are initiators, attempting to become a leader
    - "passive" nodes have selected smaller id's than "active" nodes and cannot
    compete for leadership anymore
    - "leader" node has won an election round, only one such node should be
    present in the network
    """

    active = 1
    passive = 2
    leader = 3

class ChangRobertsMessageHeader(GenericMessageHeader):
    def __init__(
            self,
            messagefrom,
            messageto,
            messagetype="Chang Roberts Message",
            nexthop=float("inf"),
            interfaceid=float("inf"),
            sequencenumber=-1,
    ):
        super().__init__(
            messagetype, messagefrom, messageto, nexthop, interfaceid, sequencenumber
        )

class ChangRobertsPayload(GenericMessagePayload):
    """
    Chang-Roberts Algorithm uses messages with one field:
    - id: The sending process id
    """
    def __init__(self, id, messagepayload=None):
        super().__init__(messagepayload)
        self.id = id


class ChangRobertsNode(GenericModel):
    """
    Node in a system that uses Chang Roberts algorithm
    Each process has three parameters:
    - id: 1 <= i <= N where N is the ring size
    - state: from State enum, active nodes participate in the election,
    passive nodes pass messages around, leader is selected when the message
    with the id of the node is arrived to the node itself
    """
    # componentname = "ChangRoberts Node Comp Name"
    # componentinstancenumber = 0
    ring_size = 0
    callback = None
    draw_delay = None
    global_round = 1
    id_counter = 0

    def __init__(self, componentname, componentinstancenumber, context=None, configurationparameters=None, num_worker_threads=1, topology=None, child_conn=None, node_queues=None, channel_queues=None):
        super().__init__(componentname, componentinstancenumber, context, configurationparameters, num_worker_threads, topology, child_conn, node_queues, channel_queues)


        """The component instance number will be used as a candidate leader process id"""
        self.id = componentinstancenumber

        """Initially all processes are active"""
        self.state = State.active

    def send_election_packet(self):
        header = ChangRobertsMessageHeader(
            messagefrom=self.componentinstancenumber,
            messageto=self.next_hop,
            messagetype="Chang Roberts Message",
            nexthop=self.next_hop,
            interfaceid=self.next_hop_interface_id

        )

        payload = ChangRobertsPayload(
            self.id
        )

        message = GenericMessage(header, payload)
        self.send_down(Event(self, EventTypes.MFRT, message))

    # def on_init(self):
    def on_init(self, eventobj: Event):
        # Select an id for round 1
        # self.id_p = randint(1, self.ring_size)
        self.id_p = self.id_counter
        self.id_counter += 1
        print(
            f"🤖 {self.componentinstancenumber} selected {self.id} as their ID."
        )

        # Calculate the neighbour, we're on a directed ring
        self.neighbour_id = (int(self.componentinstancenumber) + 1) % self.ring_size

        self.next_hop = self.topology.get_next_hop(
            self.componentinstancenumber, self.neighbour_id
        )

        self.next_hop_interface_id = f"{self.componentinstancenumber}-{self.next_hop}"

        if(self.id_p == 0):
            self.send_election_packet()

    
    def pass_packet_along(self, message):
        """For passive processes

        :message: the whole Event, with eventcontent which includes header and
        payload

        """
        pass


    def on_message_from_bottom(self, eventobj: Event):
        """New message from """
        payload: ChangRobertsPayload = eventobj.eventcontent.payload
        header: ChangRobertsMessageHeader = eventobj.eventcontent.header

        message_assumed_id = payload.id

        # For active node, we are going to follow if/else chain

        if self.state == State.passive:
            # passive node, pass the message on to the next hop
            # header will be updated
            # payload will remain unchanged

            header.messageto = self.next_hop
            header.nexthop = self.next_hop
            header.interfaceid = self.next_hop_interface_id

            message = GenericMessage(header, payload)
            self.send_down(Event(self, EventTypes.MFRT, message))

        elif self.state == State.active:

            if message_assumed_id > self.id:
                # Another node has a higher id than this node
                # going passive

                print(
                    f"🤖 {self.componentinstancenumber} is PASSIVE: {message_assumed_id} is encountered, this node is at {self.id}"
                )

                self.state = State.passive
                
                header.messageto = self.next_hop
                header.nexthop = self.next_hop
                header.interfaceid = self.next_hop_interface_id

                message = GenericMessage(header, payload)
                self.send_down(Event(self, EventTypes.MFRT, message))

            elif message_assumed_id < self.id:
                # This node has received a message with a lower assumed id
                # So, this node can dismiss the election attempt of the sender node
                # the message will be updated with this node's id

                print(
                    f"🤖 {self.componentinstancenumber} is dismissing {message_assumed_id} that is encountered. This node is at {self.id}"
                )

                payload.id = self.componentinstancenumber
                header.messageto = self.next_hop
                header.nexthop = self.next_hop
                header.interfaceid = self.next_hop_interface_id

                message = GenericMessage(header, payload)
                self.send_down(Event(self, EventTypes.MFRT, message))


            elif(
                message_assumed_id == self.id
            ):
                # This node is selected as leader
                self.state = State.leader
                print(
                    f"🤖 {self.componentinstancenumber}: I'M THE ELECTED LEADER"
                )
                ChangRobertsNode.global_round = 3
            

        self.callback.set()
        self.draw_delay.wait()
        self.draw_delay.clear()