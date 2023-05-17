import socket, multiprocessing 
#import logging
import csv, os
import re

if __name__ == "__main__" :

    # création et écoute du socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #AF_INET=IPv4,SOCK_STREAM=TCP
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 4000))   # on écoute toutes les interfaces. On peut mettre un  nom de domaine à la place de l'ip mais pas fiable pcq Py recupere la premiere IP donnée par le process de resolution de nom
        s.listen(10)     # (10 connexions en attente tolérée)
    #If your server receives a lot of connection requests simultaneously, increasing the backlog value may help by setting the maximum length of the queue for pending connections.
    #The maximum value is system dependent. For example, on Linux, see
    #https://serverfault.com/questions/518862/will-increasing-net-core-somaxconn-make-a-difference/519152

        with multiprocessing.Pool(10) as pool:
            # traitement des requêtes
            while True:
                conn, address = s.accept()
                print(f"Connected by {address}")
                #table=[] #Création d'un tableau pour insertion des IP
                with conn:
                    buff = conn.recv(1024) #conn.recv 1024 -> augmentation des données recues a un max de 1024 bytes // possibilité d'appeler plusieurs fois pour être sur de recevoir toutes les data
                    print('Message reçu !')
                    message = buff.decode('utf-8')
                    #logging.basicConfig(filename="addresses.csv", level=logging.INFO, format='%(asctime)s -- %(message)s')
                    #Vérification de l'existence ou non de l'adresse IP
                    #if address[0] not in table:
                            #table.append(address[0]) #Ajout de l'ip (address = IP+PORT, donc on choisit [0]) dans le tableau
                    #logging.info("L'adresse '{}' a été enregistrée avec succès !".format(address[0]))
                    #else:
                        #print("L'adresse ip '{}' est déjà été renseignée.".format(address[0]))
                    print ('{} a envoyé : "{}"'.format(address,message))
                    
                    
                    #déclaration des élèments du fichier CSV
                    data=[
                        [address[0], message]
                    ]
                    ip="{}".format(address[0])
                    #vérification de l'existence du fichier sinon création + ajout des valeurs
                    if os.path.exists('addresses/clients/{}-address.csv'.format(message)):
                        with open('addresses/clients/{}-address.csv'.format(message), 'r', encoding="utf-8") as f:
                            f.readlines()
                            ad=re.search(ip)
                            if ad==True:
                                f.close()
                                print('{} est une IP deja enregistree.')
                            else:
                                with open('addresses/clients/{}-address.csv'.format(message), 'a', encoding="utf-8") as f:
                                    writer = csv.writer(f)
                                    writer.writerow(data)
                                    f.close()
                    else:
                        with open('addresses/clients/{}-address.csv'.format(message), 'w', encoding="utf-8") as f:
                                    writer = csv.writer(f)
                                    writer.writerow(data)
                                    f.close()
                        
                    #on vérifie si le fichier existe, sinon on le créé et on y ajoute les données
                    if os.path.exists('addresses/global/global-address.csv'):
                        with open('addresses/global/global-address.csv', 'r', encoding="utf-8") as f:
                            f.readlines()
                            ad=re.search(ip)
                            if ad==True:
                                f.close()
                                print('{} est une IP deja enregistree.')
                            else:
                                with open('addresses/global/global-address.csv', 'a', encoding="utf-8") as f:
                                    writer = csv.writer(f)
                                    writer.writerow(data)
                                    f.close()
                    else:
                        with open('addresses/global/global-address.csv'.format(message), 'w', encoding="utf-8") as f:
                                    writer = csv.writer(f)
                                    writer.writerow(data)
                                    f.close()
                            
                    #print(table)
                    
                    
                    # réponse au client
                    conn.sendall(str.encode("Connexion recue ! Adresse ip enregistree pour l'utilisateur {}.".format(message))) #sendall permet d'envoyer la totalitées des données ou jusqu'à l'erreur. send() s'arrete à un montant donné de données.
                    
                    #reception adresse mac de machine connectée, et comparaison de l'IPv4 recue avec celle deja enregistrée et action ensuite