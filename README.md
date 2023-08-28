# Console-Messenger
Console Messenger created by Patryk 'UltiPro' Wójtowicz using Python and RSA encryption.

Server-client application for console communication. The application uses the RSA algorithm (1024 bit length) to encrypt communication. The application has a rich palette of commands, which you can read below. In addition, information about banned users is saved, administrators are not saved due to the lack of authentication in the application, which could result in impersonating an unconnected administrator. Nicknames shorter than 3 characters and longer than 24 characters are not allowed. Two or more users cannot have the same nickname. Single message cannot be longer than 128 characters and shorter than 1 character. The application has lots of colorful communications to understand what is going on during app is running. Communication and system errors are also handled, allowing you to use the application smoothly. Warning! Application tested only on Windows 10!

# Dependencies and Usage

Dependencies:

<ul>
  <li>colorama 0.4.6</li>
  <li>mpmath 1.3.0</li>
  <li>sympy 1.12</li>
</ul>

Installation:

> cd "/Console Messenger"

> pip install -r requirements.txt

## Server Side

### Using the app

> python server.py [ip-address] [port]

> python server.py [ip-address]

> python server.py

### Default values

| Property      | Value         |
| ------------- | ------------- |
| ip-address    | 127.0.0.1     |
| port          | 50500         |

### Commands

> /stop -> Closes server.

> /clear -> Clears console.

> /msg [message] -> Sends server message to all.

> /kick [nickname] -> Kicks user from server.

> /admin [nickname] -> Gives user admin permissions.

> /unadmin [nickname] -> Takes off user admin permissions.

> /ban [nickname] -> Bans user from server.

> /unban [nickname] -> Unbans user from server.

> /list u -> Prints list of connected users.

> /list a -> Prints list of connected users with admin permissions.

> /list b -> Prints list of banned users.

> /help -> Prints commands informations.

## Client Side

### Using the app

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

> /stop -> Closes application.

> /clear -> Clears console.

> /pv [nickname] [message] -> Sends a private message to the specified user.

> /kick [nickname] -> Kicks user from server. (requires admin permissions)

> /ban [nickname] -> Bans user from server. (requires admin permissions)

> /unban [nickname] -> Unbans user from server. (requires admin permissions)

> /list u -> Prints list of connected users.

> /list a -> Prints list of connected users with admin permissions.

> /list b -> Prints list of banned users.

> /help -> Prints commands informations.

# Preview

### Server

![Server preview](/screenshots/Server.png)

### Client 1

![Client 1 preview](/screenshots/Client1.png)

### Client 2

![Client 2 preview](/screenshots/Client2.png)

### Client 3

![Client 3 preview](/screenshots/Client3.png)

### Client 4

![Client 4-1 preview](/screenshots/Client4-1.png)

![Client 4-2 preview](/screenshots/Client4-2.png)

![Client 4-3 preview](/screenshots/Client4-3.png)
