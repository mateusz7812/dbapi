# modular_server
It is project of modular server, which allow on fast and easy adding new action options.

The file "Main" organises all classes of the project.
Requests are taking by http protocol, it results from that currently is only one "Taker" class - TwistedTaker.
Next they are being redirected by "Forwarder" class to "Processor" classes, which are doing tasks from requests and returning response.

A server in this repository is configured to handle users accounts and lists managing.
The project is including unit and functionals tests.
