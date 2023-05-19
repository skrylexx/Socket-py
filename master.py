import socket, multiprocessing 
#import logging
import csv, os
import re
import secrets, string

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
                #Création d'un identifiant random 
                """"
                lower = string.ascii_lowercase
                upper = string.ascii_uppercase
                numbers = string.digits
                alphabet = lower + upper + numbers
                id_lenght = 8
                id_socket = ''
                for i in range(id_lenght):
                    id_socket += ''.join(secrets.choice(alphabet))
                #print(id_socket)
                #Vérification de l'existance ou non de l'id dans le fichier de log
                with open('socket_ids.csv', 'r', encoding='utf-8') as r:
                    csv_reader = csv.reader(r)
                    for row in r:
                        if id_socket in row:
                            print('Machine d')
                    return False
                """

                with conn:
                    buff = conn.recv(1024) #conn.recv 1024 -> augmentation des données recues a un max de 1024 bytes // possibilité d'appeler plusieurs fois pour être sur de recevoir toutes les data
                    print('Données reçues !')
                    #print(type(address[0]))
                    message = buff.decode('utf-8')
                    #logging.basicConfig(filename="addresses.csv", level=logging.INFO, format='%(asctime)s -- %(message)s')
                    #Vérification de l'existence ou non de l'adresse IP
                    #if address[0] not in table:
                            #table.append(address[0]) #Ajout de l'ip (address = IP+PORT, donc on choisit [0]) dans le tableau
                    #logging.info("L'adresse '{}' a été enregistrée avec succès !".format(address[0]))
                    #else:
                        #print("L'adresse ip '{}' est déjà été renseignée.".format(address[0]))
                    print ('{} a envoyé : "{}"'.format(address[0],message))
                    
                    
                    #vérification de l'existence du fichier sinon création
                    if os.path.exists('addresses/clients/{}-address.csv'.format(message)):
                        pass
                    else:
                        with open('addresses/clients/{}-address.csv'.format(message), 'w', encoding="utf-8") as f:
                            f.close()
                            
                    if os.path.exists('addresses/global/global-address.csv'):
                        pass
                    else:
                        with open('addresses/global/global-address.csv', 'w', encoding="utf-8") as f:
                            f.close()
                    
                    
                    #fonctions de recherche d'un element dans les fichiers csv
                    def global_fonc(global_path, search_element):
                        with open(global_path, 'r') as csv_file:
                            csv_reader = csv.reader(csv_file)
                            for row in csv_reader:
                                if search_element in row:
                                    return True
                            return False
                        
                    def client_fonc(client_path, search_element):
                        with open(client_path, 'r') as csv_file:
                            csv_reader = csv.reader(csv_file)
                            for row in csv_reader:
                                if search_element in row:
                                    return True
                            return False
                    
                    def name_fonc(global_path, pseudo_search):
                        with open(global_path, 'r') as csv_file:
                            csv_reader = csv.reader(csv_file)
                            for row in csv_reader:
                                if pseudo_search in row:
                                    return True
                            return False
                    
                    #déclaration des élèments du fichier CSV
                    #ip_client=socket.inet_aton(address[0])
                    #ip_client=str(address[0], 'utf-8')
                    ip_client=address[0]
                    data=[
                        [ip_client, message]
                    ]
                    client_path = 'addresses/clients/{}-address.csv'.format(message)
                    global_path = 'addresses/global/global-address.csv'
                    search_element = address[0]
                    pseudo_search = message
                    client_present = client_fonc(client_path, search_element)
                    global_present = global_fonc(global_path, search_element)

                    if client_present:
                        print(f"L'adresse ip {search_element} est déjà renseignée dans le fichier.")
                    else:
                        with open('addresses/clients/{}-address.csv'.format(message), 'a', encoding="utf-8") as f:
                            writer = csv.writer(f)
                            writer.writerow(data)
                            f.close()
                        
                    if global_present==True:
                        print(f"L'adresse ip {search_element} est déjà renseignée dans le fichier.")
                    elif name_fonc==True:
                        print(f"L'adresse ip pour l'utilisateur '{message}' a déjà été enregistrée.")
                    else:
                        with open('addresses/global/global-address.csv', 'a', encoding="utf-8") as f:
                            writer = csv.writer(f)
                            writer.writerow(data)
                            f.close()
                                

                    # réponse au client
                    conn.sendall(str.encode("Connexion recue ! Adresse ip enregistree pour l'utilisateur {}.".format(message))) #sendall permet d'envoyer la totalitées des données ou jusqu'à l'erreur. send() s'arrete à un montant donné de données.
                    
                    #reception adresse mac de machine connectée, et comparaison de l'IPv4 recue avec celle deja enregistrée et action ensuite