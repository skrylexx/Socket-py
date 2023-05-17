import socket, multiprocessing, logging

# message
msgClient = input("Votre nom d'utilisateur : ")
msgToSend = str.encode(msgClient)

# création du socket TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    # connexion et envoi
    s.connect(("127.0.0.1", 4000))
    s.sendall(msgToSend) #sendall() -> envoie jusqu'à la fin ou une erreur, send() -> envoie un nb donné de données
    #byte=socket.inet_aton(IP) Traduit la string IP en byte pour le socket
    #s.sendall(byte) supposé renvoi de l'adresse ip
    
    # réponse du serveur
    msgServer = s.recv(1024).decode() #s.recv 1024 -> augmentation des données recues a un max de 1024 bytes // possibilité d'appeler plusieurs fois pour être sur de recevoir toutes les data
    print("Le serveur a répondu : {}".format(msgServer))
    s.close
    #ajout adresse mac à envoyer au master pour qi'il compare l'IP qu'il a avec celle reçue