Secure Application Development & Optimization

Author: Mayukh Biswas
Student ID: 23010348221
Department: Department of Cyber Science and Technology

📌 Project Overview

This repository contains the advanced implementations, security audits, and concurrency optimizations developed during Assignment 8 of ISEA Phase 3. The project successfully transitions our cryptographic chat application from a basic multi-threaded prototype into an enterprise-grade, high-concurrency daemon equipped with automated heartbeat monitoring, decoupled configuration management, graceful OS signal shutdown, and automated performance benchmarking.

📂 Repository Structure

├── server.py                 # Multi-threaded server daemon with ThreadPoolExecutor
├── client.py                 # Tkinter-based secure GUI chat client
├── config.json               # Decoupled system configuration file
├── user_credentials.json     # Encrypted user authentication database
├── chat_history.csv          # Encrypted/Structured session chat log
├── security_log.csv          # Real-time security audit logging
├── performance_results.csv   # Automated performance metrics capture
├── graphs/                   # Auto-generated performance visualization plots
│   ├── delay_vs_clients.png
│   ├── throughput_vs_clients.png
│   └── resource_usage.png
├── screenshot/               # Execution evidence and Wireshark captures
├── Assignment 8 Report.pdf     # Comprehensive LaTeX technical report source & build
└── README.md                 # Project documentation

🚀 Key Features & Task Breakdown

ThreadPool Concurrency Control (Task 3): Replaced unbounded thread spawning with a controlled ThreadPoolExecutor ($N_{\text{workers}} = 20$) to prevent CPU starvation and socket exhaustion under high loads.
Decoupled Configuration (Task 4): All network ports, timeouts, buffer sizes, and storage paths are externalized into config.json for runtime flexibility.
Connection Management & Heartbeats (Task 1): Implemented a background ping-pong mechanism ($\Delta t = 10\text{ s}$) to detect stale sockets and clean up ghost connections.
Graceful Shutdown (Task 2): Signal handlers (SIGINT, SIGTERM) ensure clean port release, final log flushing, and client notification on exit.
Automated Benchmarking & Logging (Task 5 & 6): Real-time tracking of latency, throughput, CPU %, and memory footprint saved to CSV and visualized using Matplotlib inside graphs/.

🛠️ Installation & Execution

1. Clone the Repository
git clone https://github.com/mayukhbiswas01/SECURE_CHAT.git
cd SECURE_CHAT

2. Configure Settings

Modify config.json to suit your network parameters:
{
    "server": {
        "host": "0.0.0.0",
        "port": 5000,
        "max_clients": 15,
        "thread_pool_workers": 20,
        "socket_timeout": 5.0,
        "ping_interval": 10
    },
    "client": {
        "server_ip": "127.0.0.1",
        "server_port": 5000,
        "reconnect_attempts": 5,
        "reconnect_delay": 3,
        "buffer_size": 4096
    }
}

3. Run the Server

python3 server.py

4. Run the Client GUI

python3 client.py

📊 Performance & Wireshark Verification

Wireshark Analysis: Captured on interface s1-eth1 verifying TCP 3-way handshakes, data payloads (PSH, ACK), and policy resets (RST).
Benchmarking: Empirical testing demonstrates stable CPU utilization (< 7.5%) and linear latency scaling across concurrent client connections.
Developed as part of the ISEA Phase 3 Cyber Security Engineering curriculum.
