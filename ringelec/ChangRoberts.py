class ChangRobertsNode(GenericModel):
    def __init__(self, componentname, componentinstancenumber, context=None, configurationparameters=None, num_worker_threads=1, topology=None):
        super().__init__(componentname, componentinstancenumber, context, configurationparameters, num_worker_threads, topology)
        self.id = componentinstancenumber
        self.state = "idle"  # Possible states: "idle", "candidate", "elected", "leader"
        self.leader_id = None  # To store the leader id
        self.max_message_id = None  # To store the maximum message id received

    def initiate_election(self):
        self.state = "candidate"
        # Send election message with its own id
        message_payload = ChangRobertsMessagePayload(self.id)
        message_header = GenericMessageHeader(ChangRobertsMessageTypes.ELECTION, self.id, (self.id + 1) % self.topology.size)
        message = GenericMessage(message_header, message_payload)
        self.send_down(Event(self, EventTypes.MFRT, message))

    def on_message_from_bottom(self, eventobj: Event):
        message = eventobj.eventcontent
        if message.header.messagetype == ChangRobertsMessageTypes.ELECTION:
            payload = message.payload
            if payload.node_id > self.id:
                # Forward the election message
                next_node_id = (self.id + 1) % self.topology.size
                message.header.messagefrom = self.id
                message.header.messageto = next_node_id
                self.send_down(Event(self, EventTypes.MFRT, message))
            elif payload.node_id < self.id:
                # Ignore the message, as it's from a lower id node
                pass
            else:
                # This node wins the election
                self.state = "elected"
                self.leader_id = self.id
                # Send leader message to all nodes
                leader_message_payload = ChangRobertsMessagePayload(self.id)
                leader_message_header = GenericMessageHeader(ChangRobertsMessageTypes.LEADER, self.id, None)
                leader_message = GenericMessage(leader_message_header, leader_message_payload)
                self.send_down(Event(self, EventTypes.MFRT, leader_message))
        elif message.header.messagetype == ChangRobertsMessageTypes.LEADER:
            self.state = "leader"
            self.leader_id = message.header.messagefrom
