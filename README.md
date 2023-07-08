# Console-Messenger
Console Messenger created by Patryk 'UltiPro' Wójtowicz using Python and RSA encryption.

Server and client application for communication in the console.

# Dependencies and Installation

The project uses:
<ul>
  <li>colorama</li>
</ul>

> Command to install dependencies: python -m pip install -r requirements.txt

## Server Side

### Usage Options

> python server.py [ip-address] [port]

> python server.py [ip-address]

> python server.py

### Default values
> ip-address = 127.0.0.1<br/>
> port = 50500

### Help in console app
> /help

## Client Side

### Usage

> python client.py [nickname] [ip-address] [port]

#### or

> python client.py [nickname] [ip-address]

#### or

> python client.py [nickname]

#### or

> python client.py

#### Default values
>nickname = Undefined<br/>
>ip-address = 127.0.0.1<br/>
>port = 50500

#### Help in console app
> /help

## Example of usage

##### Server

![Console server usage](/screenshots/server.png)

##### Client 1

![Console user1 usage](/screenshots/chat1.png)

##### Client 2

![Console user2 usage](/screenshots/chat2.png)
