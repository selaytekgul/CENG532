class ChangRobertsMessagePayload(GenericMessagePayload):
    def __init__(self, uid, direction, messagepayload=None):
        super().__init__(messagepayload)
        self.uid = uid
        self.direction = direction

class ChangRobertsNode(GenericModel):
    def __init__(self, componentname, componentinstancenumber, context=None, configurationparameters=None, num_worker_threads=1, topology=None):
        super().__init__(componentname, componentinstancenumber, context, configurationparameters, num_worker_threads, topology)
        self.uid = int(componentinstancenumber)
        self.neighbour_id = (self.uid % topology.num_nodes) + 1 if self.uid < topology.num_nodes else 1
        self.next_hop = topology.get_next_hop(self.uid, self.neighbour_id)
        self.next_hop_interface_id = f"{self.uid}-{self.next_hop}"

    def initiate_election(self):
        header = ChangRobertsMessageHeader(
            messagefrom=self.componentinstancenumber,
            messageto=self.next_hop,
            nexthop=self.next_hop,
            messagetype="Chang-Roberts Message",
            interfaceid=self.next_hop_interface_id
        )
        payload = ChangRobertsMessagePayload(self.uid, "clockwise")
        message = GenericMessage(header, payload)
        self.send_down(Event(self, EventTypes.MFRT, message))

    def on_message_from_bottom(self, eventobj: Event):
        payload: ChangRobertsMessagePayload = eventobj.eventcontent.payload
        header: ChangRobertsMessageHeader = eventobj.eventcontent.header

        if payload.uid == self.uid:
            # Election completed
            logger.debug(f"🤖 {self.componentinstancenumber}: I'm the leader!")
        else:
            if payload.direction == "clockwise":
                if payload.uid < self.uid:
                    # Forward message clockwise
                    payload.direction = "clockwise"
                    header.messageto = self.next_hop
                    header.next_hop = self.next_hop
                    header.interfaceid = self.next_hop_interface_id
                    message = GenericMessage(header, payload)
                    self.send_down(Event(self, EventTypes.MFRT, message))
                else:
                    # Send message in reverse direction
                    payload.direction = "counterclockwise"
                    header.messageto = self.topology.get_previous_hop(self.componentinstancenumber, self.neighbour_id)
                    header.next_hop = header.messageto
                    header.interfaceid = f"{self.componentinstancenumber}-{header.messageto}"
                    message = GenericMessage(header, payload)
                    self.send_down(Event(self, EventTypes.MFRT, message))
            else:
                if payload.uid > self.uid:
                    # Forward message counterclockwise
                    payload.direction = "counterclockwise"
                    header.messageto = self.next_hop
                    header.next_hop = self.next_hop
                    header.interfaceid = self.next_hop_interface_id
                    message = GenericMessage(header, payload)
                    self.send_down(Event(self, EventTypes.MFRT, message))
                else:
                    # Send message in reverse direction
                    payload.direction = "clockwise"
                    header.messageto = self.topology.get_previous_hop(self.componentinstancenumber, self.neighbour_id)
                    header.next_hop = header.messageto
                    header.interfaceid = f"{self.componentinstancenumber}-{header.messageto}"
                    message = GenericMessage(header, payload)
                    self.send_down(Event(self, EventTypes.MFRT, message))

