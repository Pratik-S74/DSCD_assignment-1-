This is a simple YouTube notification system implemented using RabbitMQ messaging broker. The system consists of three components: Youtube-server.py, Youtuber.py, and User.py. The server handles user login, subscription, and video upload notifications. Youtubers can upload videos, and users can subscribe to receive notifications for new videos.

Requirements:-

    Python 3.x
    RabbitMQ Server
    
Setup:-

1) Install RabbitMQ Server:
     Follow the official installation guide to install RabbitMQ on your system.
2) Install required Python packages:
     pip install pika

Running the Program:-

1. Start RabbitMQ Server:
2. Run Youtube-server.py:
	python Youtube-server.py
3. Run Youtuber.py:
	python Youtuber.py <youtuber_name> <video_name>
4. Run User.py:
	python User.py <user_name> <s (subscribe) or u (unsubscribe)> <youtuber_name>


Important Notes:-

1) Make sure to run RabbitMQ server before executing any of the scripts.
2) Ensure that the RabbitMQ server is running on localhost.
3) The program uses separate queues for each user to deliver notifications.
4) Terminate the scripts using Ctrl+C when done.
