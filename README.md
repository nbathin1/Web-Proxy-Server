Here’s a README file for your Web Proxy Server project based on the document you provided:

Web Proxy Server

Overview

This project involves the implementation of a multi-threaded web proxy server that acts as an intermediary between a client and a web server. The project is divided into two parts:

	1.	Part 1: Basic proxy functionality where the proxy forwards requests and responses between the client and the server.
	2.	Part 2: Caching functionality, where the proxy caches server responses to improve performance.

Key Features:

	•	Multi-threaded implementation using Python.
	•	Proxy server forwards requests from the client to the server and sends the response back.
	•	Caching responses for 120 seconds, allowing the proxy to return cached content without contacting the server if the cached data is valid.

Part 1: Proxy Server without Caching

In this part, the proxy server acts as an intermediary between the client and the server:

	•	Forwards client requests to the server.
	•	Forwards server responses back to the client.
	•	Prints log information to the terminal indicating the destination (client or server), thread ID, and timestamp.

Log Format:

proxy-forward, DESTINATION, THREAD-ID, TIMESTAMP

	•	DESTINATION: Can be either “client” or “server”.
	•	THREAD-ID: The ID of the thread processing the request.
	•	TIMESTAMP: The exact time when the request or response was forwarded.

Example Log:

proxy-forward,server,12345,2022-11-29 12:34:56
server-response,12345,2022-11-29 12:34:57

Part 2: Proxy Server with Caching

In the second part, the proxy server caches server responses for 120 seconds:

	•	When a client makes a request, the proxy checks if the requested content is already cached and valid.
	•	If the cached content is valid (not older than 120 seconds), the proxy returns the cached content without contacting the server.
	•	If the content is not cached or has expired, the proxy fetches it from the server, caches it, and then returns the response to the client.

Cache Hit Log Format:

proxy-cache, client, THREAD-ID, TIMESTAMP

Caching Details:

	•	Cached content is stored on disk.
	•	The proxy maintains an internal data structure to track which objects are cached and where they are stored on disk.
	•	Cached responses are considered invalid after 120 seconds.

Example Cache Log:

proxy-cache,client,54321,2022-11-29 12:36:12

Implementation Files:

	•	webserver1.py: Implementation of the basic web server.
	•	proxyserver1.py: Proxy server implementation for part 1 (without caching).
	•	proxyserver2.py: Proxy server implementation for part 2 (with caching).
	•	Screenshots: Verification screenshots for proxy and web server logs.

How to Run:

	1.	Set up the environment: Ensure Python 3 is installed.
	2.	Run the web server:

python3 webserver1.py


	3.	Run the proxy server (Part 1 - No caching):

python3 proxyserver1.py


	4.	Run the proxy server (Part 2 - With caching):

python3 proxyserver2.py


	5.	Client: Use a web browser to make HTTP requests through the proxy server.

Testing:

	•	The proxy server and web server should be run from different directories when testing on the same device.
	•	Use the provided HTML templates to generate different test web pages.
	•	Verify functionality by checking the logs printed in the terminal and inspecting the output in the client’s browser.

Logs:

Logs will be printed in the terminal, showing the status of requests and responses in the following format:

	•	proxy-forward, DESTINATION, THREAD-ID, TIMESTAMP
	•	server-response, THREAD-ID, TIMESTAMP
	•	proxy-cache, client, THREAD-ID, TIMESTAMP

Authors:

	•	Nikhil Bathini

