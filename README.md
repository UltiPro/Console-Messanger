# Console-Messenger
Console Messenger created by Patryk 'UltiPro' Wójtowicz using Python and RSA encryption.

Server and client application for communication in the console.

# Dependencies and Installation

Dependencies:

<ul>
  <li>colorama</li>
</ul>

Installation:

> pip install -r requirements.txt

# Server Side

### Usage

> python server.py [ip-address] [port]

> python server.py [ip-address]

> python server.py

### Default values

| Property      | Value         |
| ------------- | ------------- |
| ip-address    | 127.0.0.1     |
| port          | 50500         |

### Commands

> /help

> /server-stop

> /server-clear

> /kick [nickname]

# Client Side

### Usage

> python client.py [nickname] [ip-address] [port]

> python client.py [nickname] [ip-address]

> python client.py [nickname]

> python client.py

### Default values

| Property      | Value         |
| ------------- | ------------- |
| nickname      | User          |
| ip-address    | 127.0.0.1     |
| port          | 50500         |

### Commands

> /help

> /client-stop

> /client-clear

# Preview

### Server

![Server preview](/screenshots/Server.png)

### Client 1

![Client 1 preview](/screenshots/Client-1.png)

### Client 2

![Client 2 preview](/screenshots/Client-2.png)
