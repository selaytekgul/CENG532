from enum import Enum
from collections import defaultdict
from adhoccomputing.Experimentation.Topology import Topology
from adhoccomputing.GenericModel import GenericModel, GenericMessageHeader,  GenericMessage
from adhoccomputing.Generics import *
from Snapshot.Snapshot import SnapshotComponentModel, SnapshotMessageTypes, SnapshotEventTypes

class FranklinMessagePayload(GenericMessagePayload):
    def __init__(self, uid, messagepayload=None):
        super().__init__(messagepayload)
        self.uid = uid

class FranklinNode(GenericModel):
    def __init__(self, componentname, componentinstancenumber, context=None, configurationparameters=None, num_worker_threads=1, topology=None):
        super().__init__(componentname, componentinstancenumber, context, configurationparameters, num_worker_threads, topology)
        self.uid = int(componentinstancenumber)
        self.has_token = self.uid == 1
        self.next_hop = (self.uid % topology.num_nodes) + 1 if self.uid < topology.num_nodes else 1
        self.next_hop_interface_id = f"{self.uid}-{self.next_hop}"

    def send_token(self):
        header = FranklinMessageHeader(
            messagefrom=self.componentinstancenumber,
            messageto=self.next_hop,
            nexthop=self.next_hop,
            messagetype="Franklin Message",
            interfaceid=self.next_hop_interface_id
        )
        payload = FranklinMessagePayload(self.uid)
        message = GenericMessage(header, payload)
        self.send_down(Event(self, EventTypes.MFRT, message))

    def on_message_from_bottom(self, eventobj: Event):
        payload: FranklinMessagePayload = eventobj.eventcontent.payload
        header: FranklinMessageHeader = eventobj.eventcontent.header

        if payload.uid == self.uid:
            # Token returned, process completed
            logger.debug(f"🤖 {self.componentinstancenumber}: I have the token!")
        elif self.has_token:
            # Pass the token to the next node
            self.has_token = False
            header.messageto = self.next_hop
            header.next_hop = self.next_hop
            header.interfaceid = self.next_hop_interface_id
            message = GenericMessage(header, payload)
            self.send_down(Event(self, EventTypes.MFRT, message))
        else:
            # Token not here, forward the message
            header.messageto = self.next_hop
            header.next_hop = self.next_hop
            header.interfaceid = self.next_hop_interface_id
            message = GenericMessage(header, payload)
            self.send_down(Event(self, EventTypes.MFRT, message))

