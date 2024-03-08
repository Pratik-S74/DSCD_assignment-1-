--> This is a simple low level group messaging app created by using ZEROMQ messaging library and socket APIs. for data serialization and deserialization in some instances JSON library was utilized.

--> Requirements:-

    Python 3.x
    ZEROMQ library
    
--> Setup:-

	1install ZEROMQ library:
	  pip install pyzmq
		

--> Running the Program:-

	1. Start ZEROMQ Server:
	
	2. Run server.py:
		python server.py
	3. Run groups.py:
		python groups.py
	4. Run user1.py:
		python user1.py
	5. Run user2.py:
		python user2.py


--> NOTES:
	- In groups.py it can either communicate to server.py via sending strings or listen to incoming requests by users.
	
	- Menu like options are provided for different functionality in user1.py and user2.py
	
	- between server.py and groups.py REQ-REP sockets were used and between groups.py and users DEALER sockets were used.
	
