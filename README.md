# UDP-Socket-Programming

A simple chat room application that allows users to exchange messages online and in real-time. This application is built using Python and utilizes the UDP transport protocol. It is compatible with Windows and Linux-based operating systems.

## Requirements

- Python
- Access to a terminal or command prompt

## Getting Started

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/<your-github-username>/<repository-name>.git
   cd <repository-name>

2. **Prepare the Environment**
   ```bash
   python --version

## Files in the Repository

- server.py : The server file that initializes and manages the chat room.
- client.py : The client file that connects to the chat room and allows the user to send and receive messages.

## How to Run the Application
The application has two main components: the server and the client.

### 1. Running the Server.py
1. Open a terminal window.
2. Navigate to the directory containing server.py.
3. Start the server using the following command:
   ```bash
   python server.py
4. The server will start and listen for incoming client connections. Make note of the IP address and port where the server is running, as the client will need these to connect.

### 2. Running the Client.py
1. Open a terminal window.
2. Navigate to the directory containing client.py.
3. Start the server using the following command:
   ```bash
   python client.py
4. When prompted, enter the IP address and port number of the server to connect to the chat room.
5. You will be asked to enter a username and chatroom password. This information is required to connect to the chat room. Enter a unique username and the correct password to proceed.

Once connected, you can begin exchanging messages with other clients who are also connected to the server. Messages are sent and received via the GUI, and you can type your messages in the provided input field.

## How It Works
- The server listens for client connections using the UDP protocol.
- Each client must enter a username and the chatroom password before connecting. The username helps identify users in the chat room, and the password is used to control access.
- Each client can send messages to the server, which then broadcasts the message to all connected clients.
- To exit the chat, press QUIT. This will disconnect the client from the server and close the application.

## Collaborators
- Florecita Natawirya - 18223040
- Gabriela Jennifer Sandy - 18223092
