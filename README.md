# iotschoolproj

Specify a protocol that communicates over UDP with an Internet of Things (IoT) device, a light bulb. The protocol must allow a client program to perform the following operations on a light bulb server:

1.Turn the light bulb on and set the color (if the light bulb is already onand color the same, the operation should work without error)

2.Change the light color 

3.Determine the status of the light: on/off, color

4.Turn the light off (If the light bulb is already off, the operation shouldworkwithout error)


The protocol must include a mechanism for:

1.Error reporting:  e.g. the bulb is not functioning, color specified is not supported, message format is not recognized

2.Reliability: Provide a response that the operation worked successfully.  Also specify the behavior of the clientwhen no response is received.


The protocol must specify:

1.Message Format (fields in the message, size in bytes, possible values)

2.Message Semantics (what function each message type performs, and possible results)

3.Trace output that client and server programs must print to demonstrate the program is working including examples.

4.Command-line arguments that specify IP address and port the server is running on and enable any test case to be executed (in arbitrary order)
