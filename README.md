Secure Multi-Client TCP Chat Application

An enterprise-grade, secure multi-client desktop chat application built using Python's socket  and
tkinter  libraries, deployed and validated inside a Mininet network virtualization environment.

This project extends the GUI-based chat from Assignment 6 by introducing critical application-
layer security mechanisms, robust session management, defensive input constraints, and
cryptographic operations.

🔒 Key Security Features Implemented
1. Client-Side SHA-256 Hashing (Task 2)

Passwords are never sent over the wire in plain text. The client hashes the password using
SHA-256 before transmitting it over the TCP socket, preventing credential sniffing.

2. IP-Based Brute Force Lockout (Task 5)

Protects against credential attacks by tracking failed login attempts per host IP. After 3
consecutive failed attempts, the offending IP is temporarily locked out for 30 seconds.

3. Duplicate Login Prevention (Task 3)

Restricts active user credentials to single concurrent sessions. Re-authenticating with an
already connected username blocks secondary handshakes immediately.

4. Active Session Timeout Sweep (Task 6)

A background daemon thread regularly audits connected sockets. If a user remains idle
(no message activity) for more than 120 seconds, the server gracefully terminates the
socket connection.

5. Strict Input Validation & Sanitization (Task 4)

Sanitizes input values on both client and server sides. Username inputs are restricted to
alphanumeric patterns (max 15 characters), and messages exceeding 500 characters are
automatically rejected.

6. Centrally Managed Secure Logs

Automatically tracks all critical network events (connections, failed logons, lockouts,
session timeouts) in a local security_log.csv  file without ever storing plain text
passwords.


📁 Repository Structure

├── server.py               # Multi-threaded secure TCP socket server
├── client_gui.py           # Modern dark-themed GUI desktop chat client
├── user_credentials.json   # Simulated user database containing SHA-256 hashes
├── security_log.csv        # Secure operational and threat event logger
├── chat_history.csv        # CSV transaction history logger (Broadcast/Private
├── README.md               # Current documentation
└── report_7.pdf            # Compiled technical evaluation report

🚀 Deployment & Execution (VM & Mininet)

Step 1: Pre-requisites & Local X11 Access

Open your VM terminal and run:

xhost +

Step 2: Initialize Mininet Network Topology

Launch a single subnet containing 5 hosts:

sudo mn --topo single,5

Step 3: Run the Secure Server (on h1)

Open a terminal window for host h1  from the Mininet console:

mininet> xterm h1

And run:

python3 server.py

Step 4: Run the Secure Clients (on h2 - h5)

Open terminal windows for the client hosts:

mininet> xterm h2 h3 h4 h5

Run the Tkinter client app on each terminal:

python3 client_gui.py expand

tune

🛡️ Security Verification (Wireshark) chat_spark

To monitor TCP transactions on port 5000, start Wireshark on the default loopback/bridge
interface:

sudo wireshark &


tcp.port == 5000

Analyze the 3-Way Handshake, SHA-256 payload transfers inside the standard PSH  frames, and
the final graceful FIN  socket teardowns on client exit.

👥 Author
Mayukh Biswas
Network Security Engineering Assignment 7


