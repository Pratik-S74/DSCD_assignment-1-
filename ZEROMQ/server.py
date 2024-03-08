import zmq
import json

class MessagingServer:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.groups = {}

    def start(self):
        self.socket.bind("tcp://*:5557")
        print("Messaging Server started!")
        while True:
            message = self.socket.recv_string()
            try:
                response = self.handle_message(message)
            except Exception as e:
                print(f"Error handling message: {e}")
                response = {"error": "Internal server error"}
            self.socket.send_string(json.dumps(response))

    def handle_message(self, message):
        parts = message.split()

        if not parts:
            return {"error": "Empty message received"}

        if parts[0] == "GET_GROUPS":
            return self.send_groups_list()
        elif parts[0] == "REGISTER_GROUP":
            if len(parts) >= 4:
                return self.register_group(parts[1], parts[2], parts[3])
            else:
                return {"error": "Insufficient parameters for REGISTER_GROUP"}
        else:
            return {"error": "Invalid input"}

    def register_group(self, group_id, ip_address, port):
        if group_id not in self.groups:
            self.groups[group_id] = {"ip_address": ip_address, "port": port}
            print(f"Group {group_id} registered: {ip_address}:{port}")
            return {"success": f"Group {group_id} registered"}
        else:
            return {"error": "Group already exists"}

    def send_groups_list(self):
        if self.groups:
            groups_list = {"groups": []}
            for group_id, group_info in self.groups.items():
                groups_list["groups"].append({"group_id": group_id, "ip_address": group_info["ip_address"], "port": group_info["port"]})
            return groups_list
        else:
            return {"message": "No groups registered yet"}

if __name__ == "__main__":
    server = MessagingServer()
    server.start()
