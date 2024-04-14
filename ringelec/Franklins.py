class FranklinNode(GenericModel):
    def __init__(self, componentname, componentinstancenumber, context=None, configurationparameters=None, num_worker_threads=1, topology=None):
        super().__init__(componentname, componentinstancenumber, context, configurationparameters, num_worker_threads, topology)
        self.id = componentinstancenumber
        self.state = "idle"  # Possible states: "idle", "probing", "coordinator"
        self.coordinator_id = None
        self.max_neighbor_id = None

    def initiate_probe(self):
        self.state = "probing"
        # Send probe message to both sides
        left_node_id = (self.id - 1) % self.topology.size
        right_node_id = (self.id + 1) % self.topology.size
        probe_message_payload = FranklinMessagePayload(self.id)
        probe_message_header_left = GenericMessageHeader(FranklinMessageTypes.PROBE, self.id, left_node_id)
        probe_message_left = GenericMessage(probe_message_header_left, probe_message_payload)
        self.send_down(Event(self, EventTypes.MFRT, probe_message_left))
        probe_message_header_right = GenericMessageHeader(FranklinMessageTypes.PROBE, self.id, right_node_id)
        probe_message_right = GenericMessage(probe_message_header_right, probe_message_payload)
        self.send_down(Event(self, EventTypes.MFRT, probe_message_right))

    def on_message_from_bottom(self, eventobj: Event):
        message = eventobj.eventcontent
        if message.header.messagetype == FranklinMessageTypes.PROBE:
            payload = message.payload
            if self.state == "idle":
                # Send ACK to the probing node
                ack_message_payload = FranklinMessagePayload(self.id)
                ack_message_header = GenericMessageHeader(FranklinMessageTypes.ACK, self.id, payload.node_id)
                ack_message = GenericMessage(ack_message_header, ack_message_payload)
                self.send_down(Event(self, EventTypes.MFRT, ack_message))
            elif self.state == "probing":
                # Compare ids to determine coordinator
                self.max_neighbor_id = max(self.max_neighbor_id, payload.node_id)
                if self.max_neighbor_id > self.id:
                    # This node becomes passive
                    self.state = "idle"
                elif self.max_neighbor_id < self.id:
                    # Send probe message again
                    self.initiate_probe()
                else:
                    # This node becomes the coordinator
                    self.state = "coordinator"
                    self.coordinator_id = self.id
                    # Send coordinator message to all nodes
                    coordinator_message_payload = FranklinMessagePayload(self.id)
                    coordinator_message_header = GenericMessageHeader(FranklinMessageTypes.COORDINATOR, self.id, None)
                    coordinator_message = GenericMessage(coordinator_message_header, coordinator_message_payload)
                    self.send_down(Event(self, EventTypes.MFRT, coordinator_message))
        elif message.header.messagetype == FranklinMessageTypes.COORDINATOR:
            self.state = "coordinator"
            self.coordinator_id = message.header.messagefrom
