'''
Comms 2
01/26/2026
'''

import bluetooth #importing libraries
import time

server = bluetooth.BluetoothSocket(bluetooth.RFCOMM) #default stuff
server.bind(("", 1))
server.listen(1)

print("Waiting for RFCOMM connection...")
client, addr = server.accept()
print("Connected from", addr)

total_bytes = 0 #default bytes arrived
interval_bytes = 0
start_time = time.time() #record time so that code knows time relative to when it started
last_report = start_time #indicate the last time cubesat reported

try:
    while True:
        data = client.recv(1024)  # blocking read
        if not data:
            print("Disconnected")
            break #end the loop if there is no data

        bytes_received = len(data) #measure length of data
        total_bytes += bytes_received #add data length to total
        interval_bytes += bytes_received #add data length to interval

        now = time.time() #record time
        if now - last_report >= 1.0: #if last report was more than 1s ago
            rate = interval_bytes / (now - last_report) #record rate of bytes sent per second
            print(f"Rate: {rate:.1f} B/s | Total: {total_bytes} bytes") #print rate and number of bytes sent
            interval_bytes = 0 #reset interval
            last_report = now #reset time

except KeyboardInterrupt: #if user presses a key
    print("Stopped by user") #stop the loop

finally: #when finished
    client.close() #close everything when done
    server.close()

def evaluate_data_arrival(received_bytes, expected_bytes, sock): #function to determine if data recieved was enough
    """
    received_bytes: int - total bytes actually received
    expected_bytes: int - total bytes expected
    sock: Bluetooth socket to ground station
    """

    if expected_bytes <= 0: #if expected bytes was nonpositive for some reason
        raise ValueError("expected_bytes must be > 0") #end the function

    ratio = received_bytes / expected_bytes #see how many bytes were received compared to expected

    if ratio > 0.5: #if more than half
        message = f"ACK: {received_bytes}/{expected_bytes} bytes received" #say how much arrived (successful)
        sock.send(message.encode()) #send the message to notify ground
        return "ACK" #say that message was successful
    else: #less than half
        message = f"RESEND: only {received_bytes}/{expected_bytes} bytes received" #say how much arrived (less than needed)
        sock.send(message.encode()) #send message to notify ground
        return "RESEND" #say that message failed
