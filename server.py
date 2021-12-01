###################################################################
#       Imported Modules
import socket
###################################################################
# In order of usefulness, I used the following sources for line 13
# https://linux.die.net/man/3/setsockopt
# https://stackoverflow.com/questions/5875177/how-to-close-a-socket-left-open-by-a-killed-program
#
def server(app):
    app.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    HOST = socket.gethostbyname(socket.gethostname()) # public ip address
    PORT = 15112
    app.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    app.server.settimeout(10)
    app.server.bind((HOST, PORT))
    app.server.listen()

###################################################################
#       Test Functions

# while True:
# communicationSocket, address = server.accept()
# print(f'Connected to {address}')
# message = communicationSocket.recv(1024).decode('utf-8')
# print(f'Message from client is {message}')
# communicationSocket.send(f'Got your message'.encode('utf-8'))
# communicationSocket.close()
# print(f'Communication with {address} completed!')

# def appStarted(app):
    
#     server(app)
#     app.partnerSocket, app.partnerAddress = app.server.accept()
#     app.message = ''
#     app.response = ''
#     app.opponentSocket, app.opponentAddress = app.server.accept()

# def keyPressed(app, event):
#     app.message += event.key
#     if len(app.message) == 2:
#         app.partnerSocket.send(app.message.encode('utf-8'))
#         app.message = ''
#         app.response = app.partnerSocket.recv(1024).decode('utf-8')
#         app.opponentSocket.send(app.message.encode('utf-8'))

# def redrawAll(app, canvas):
#     canvas.create_text(app.width//2, app.height//2,
#                         text=f'mes:{app.message}, res:{app.response}',
#                         anchor='center', font=('Ubuntu', 80, 'bold'), fill='black')

# runApp(width=1200, height=700)
