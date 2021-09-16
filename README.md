# SMTP Plugin

The purpose of this plugin is send emails using SMTP servers. The plugin supports sending HTML message.

# Configuration

This node requires configuration. In order to read timezone you must define path to time zone. Use dot notation to do
that.

* smtp: smtp.gmail.com, - Choose a smtp server 
* port: 587, - Select the port on which smtp will run 
* username: None, - enter your username 
* password: None, - enter your password 
* to: None, - Choose email recipient 
* from: None, - Choose your email 
* replyTo: None,- Select to whom the reply should be sent 
* title: Select a Title Message, 
* message: Enter your message, HTML is allowed

# Input payload

This node does not process input payload.

# Output

This is one output Mail send.
