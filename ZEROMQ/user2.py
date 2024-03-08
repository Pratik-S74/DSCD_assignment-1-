import zmq
import time
import json

class User:
    def __init__(self, uuid, port):
        self.uuid = uuid
        self.context = zmq.Context()
        self.group_socket = self.context.socket(zmq.DEALER)
        self.group_socket.connect(f"tcp://localhost:{port}")  

    def start(self):
        while True:
            message = input("Enter the input:\n  1)JOIN 2)LEAVE 3)GET_MESSAGES 4)SEND_MESSAGE 5)GET_GROUPS: ")
            parts = message.split()

            if parts[0] == "JOIN":
                group_id = parts[1]
                self.join_group(group_id)
            elif parts[0] == "LEAVE":
                group_id = parts[1]
                self.leave_group(group_id)
            elif parts[0] == "SEND_MESSAGE":
                group_id = parts[1]
                content = " ".join(parts[2:])
                self.send_message(group_id, content)
            elif parts[0] == "GET_MESSAGES":
                group_id = parts[1]
                self.get_messages(group_id)
            elif parts[0] == "GET_GROUPS":
                self.get_groups()
            else:
                print("ERROR: Invalid input string")

    def join_group(self, group_id):
        self.group_socket.send_multipart([self.uuid.encode(), b"JOIN", group_id.encode()])
        response_parts = self.group_socket.recv_multipart()
        sender_id = response_parts[0]
        response_code = response_parts[1]
        response_data = response_parts[2].decode() if len(response_parts) > 2 else ""

        if response_code == b"JOIN_GROUP_SUCCESS":
            print(f"Successfully joined group {group_id}")
        else:
            print(f"Error joining group {group_id}: {response_data}")

    def leave_group(self, group_id):
        self.group_socket.send_multipart([self.uuid.encode(), b"LEAVE", group_id.encode()])
        response_parts = self.group_socket.recv_multipart()
        sender_id = response_parts[0]
        response_code = response_parts[1]
        response_data = response_parts[2].decode() if len(response_parts) > 2 else ""

        if response_code == b"LEAVE_GROUP_SUCC":
            print(f"Successfully left group {group_id}")
        else:
            print(f"Error leaving group {group_id}: {response_data}")

    def send_message(self, group_id, content):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        message = f"{self.uuid} | {timestamp} | {content}".encode()
        self.group_socket.send_multipart([self.uuid.encode(), b"SEND_MESSAGE", group_id.encode(), message])
        response_parts = self.group_socket.recv_multipart()
        sender_id = response_parts[0]
        response_code = response_parts[1]
        response_data = response_parts[2].decode() if len(response_parts) > 2 else ""

        if response_code == b"MESSAGE_SENT":
            print(f"Message sent to group {group_id.encode()}")
        else:
            print(f"Error sending message: {response_data}")


    def get_messages(self, group_id, timestamp_str=""):
        message_parts = [self.uuid.encode(), b"GET_MESSAGES", group_id.encode()]
        if timestamp_str:
            message_parts.append(timestamp_str.encode())
        self.group_socket.send_multipart(message_parts)
        response_parts = self.group_socket.recv_multipart()
        sender_id = response_parts[0]
        response_code = response_parts[1]
        response_data = response_parts[2].decode() if len(response_parts) > 2 else ""
        # print(response_data)

        if response_code == b"MESSAGES":
            print(f"Messages from group {group_id}:\n{response_data}")
        else:
            print(f"Error getting messages: {response_data}")

    def get_groups(self):
        server_socket = self.context.socket(zmq.REQ)
        server_socket.connect("tcp://35.202.56.165:5557")
        server_socket.send_string("GET_GROUPS")
        response = server_socket.recv_string()
        print(response)
        server_socket.close()

if __name__ == "__main__":
    user = User("986b", 5560)  # Specify the port for user2.py
    user.start()
