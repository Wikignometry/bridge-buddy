###################################################################
#       Imported Modules
import socket
###################################################################
#  initial client setup

def client(app):
    app.HOST = socket.gethostbyname(socket.gethostname()) # public ip address
    app.PORT = 15112



###################################################################
#       Test Functions

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# s.connect((HOST, PORT))

# s.send('Hello World'.encode('utf-8'))


# def appStarted(app):
#     app.partnerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#     app.partnerSocket.connect((HOST, PORT))
#     app.message = ''
#     app.response = ''

# def keyPressed(app, event):
#     app.message += event.key
#     if len(app.message) == 2:
#         app.partnerSocket.send(app.message.encode('utf-8'))
#         app.message = ''
#         app.response = app.partnerSocket.recv(1024).decode('utf-8')


# def redrawAll(app, canvas):
#     canvas.create_text(app.width//2, app.height//2,
#                         text=f'mes:{app.message}, res:{app.response}',
#                         anchor='center', font=('Ubuntu', 80, 'bold'), fill='black')


# runApp(width=1200, height=700)
