import zmq
import time
import datetime
import json
import threading

class GroupServer:
    def __init__(self, message_server_host, port):
        self.message_server_host = message_server_host
        self.port = port
        self.group_port_user1 = 5559
        self.group_port_user2 = 5560
        self.context = zmq.Context()
        self.server_socket = self.context.socket(zmq.REQ)
        self.server_socket.connect(f"tcp://{message_server_host}:{port}")
        self.user_socket_user1 = self.context.socket(zmq.DEALER)
        self.user_socket_user1.bind(f"tcp://*:{self.group_port_user1}")
        self.user_socket_user2 = self.context.socket(zmq.DEALER)
        self.user_socket_user2.bind(f"tcp://*:{self.group_port_user2}")
        self.groups = {}
        self.messages = {}
        threading.Thread(target=self.start_user_connection, args=(self.user_socket_user1,)).start()
        threading.Thread(target=self.start_user_connection, args=(self.user_socket_user2,)).start()

    def start_user_connection(self, user_socket):
        while True:
            message_parts = user_socket.recv_multipart()
            sender_id = message_parts[0]
            message = message_parts[1]
            group_id = message_parts[2].decode() if len(message_parts) > 2 else ""

            if message == b"JOIN":
                self.handle_join(sender_id, group_id, user_socket)
            elif message == b"LEAVE":
                self.handle_leave(sender_id, group_id, user_socket)
            elif message == b"SEND_MESSAGE":
                self.handle_send_message(sender_id, group_id, message_parts[3:], user_socket)
            elif message == b"GET_MESSAGES":
                self.handle_get_messages(sender_id, group_id, user_socket)
            elif message == b"GET_GROUPS":
                self.server_socket.send_string("GET_GROUPS")
                response = self.server_socket.recv_string()
                print(response)
            else:
                print(f"Invalid message from {sender_id}: {message}")

    def start(self):
        while True:
            com = input("1. Enter server to send messages to server: \n2. Enter user to receive messages strings from user: \n")
            if com == 'server':
                message = input("Enter the message you want to send to server:\n 1) GET_GROUPS \t 2) REGISTER_GROUP:    ")
                self.server_socket.send_string(message)
                response = self.server_socket.recv_string()
                print("Received from the server: ", response)
            elif com == 'user':
                pass  # The user_socket threads are already handling this

    def handle_join(self, sender_id, group_id, user_socket):
        self.server_socket.send_string("GET_GROUPS")
        response = self.server_socket.recv_string()
        groups_info = json.loads(response)["groups"]
        for group_info in groups_info:
            if group_info["group_id"].strip() == group_id.strip():
                try:
                    self.groups.setdefault(group_id, {"members": set(), "messages": []})
                    self.groups[group_id]["members"].add(sender_id)
                    user_socket.send_multipart([sender_id, b"JOIN_GROUP_SUCCESS"])
                    # return
                except KeyError:
                    # print(f"Error connecting to group {group_id}: {e}")
                    user_socket.send_multipart([sender_id, b"GROUP_UNAVAILABLE"])
                    # return
            else:
                user_socket.send_multipart([sender_id, b"GROUP_UNAVAILABLE"])


    def handle_leave(self, sender_id, group_id, user_socket):
        if group_id not in self.groups:
            user_socket.send_multipart([sender_id, b"NOT_IN_GROUP"])
            return
        try:
            self.groups[group_id]["members"].remove(sender_id)
            user_socket.send_multipart([sender_id, b"LEAVE_GROUP_SUCC"])
        except KeyError:
            user_socket.send_multipart([sender_id, b"NOT_IN_GROUP"])

    def handle_send_message(self, sender_id, group_id, message_parts, user_socket):
        if group_id not in self.groups or sender_id not in self.groups[group_id]["members"]:
            user_socket.send_multipart([sender_id, b"NOT_IN_GROUP"])
            return

        try:
            timestamp = datetime.datetime.utcnow().isoformat()
            message_content = b" ".join(message_parts).decode()  # Decode the bytes to string
            message = f"{sender_id.decode()} ({timestamp}) : {message_content}".encode()  # Decode sender_id bytes to string

            self.groups[group_id]["messages"].append(message)

            # Broadcast the message to all members of the group
            if group_id in self.groups:
                for user_id in self.groups[group_id]["members"]:
                    if user_id != sender_id:
                        user_socket.send_multipart([user_id, b"MESSAGE", message])
                user_socket.send_multipart([sender_id, b"MESSAGE_SENT"])
            else:
                user_socket.send_multipart([sender_id, b"NOT_IN_GROUP"])

        except Exception as e:
            print(f"Error sending message: {e}")

    def handle_get_messages(self, sender_id, group_id, user_socket, timestamp_str=b""):
        if sender_id not in self.groups[group_id]["members"]:
            user_socket.send_multipart([sender_id, b"NOT_IN_GROUP"])
            return

        try:
            if timestamp_str:
                # Convert the timestamp string to a datetime object
                timestamp = datetime.datetime.fromisoformat(timestamp_str.decode())
            else:
                timestamp = datetime.datetime.min
        except ValueError:
            user_socket.send_multipart([sender_id, b"INVALID_TIMESTAMP"])
            return

        filtered_messages = [msg for msg in self.groups[group_id]["messages"] if datetime.datetime.fromisoformat(msg.decode().split('(')[1].split(')')[0]) > timestamp]
        message_str = "\n".join(msg.decode() for msg in filtered_messages)
        user_socket.send_multipart([sender_id, b"MESSAGES", message_str.encode()])

if __name__ == "__main__":
    port = 5557
    group = GroupServer("35.202.56.165", port)
    group.start()
