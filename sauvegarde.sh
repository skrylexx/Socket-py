#commande à effectuer pour sauvegarder les fichiers du local vers le serveur distant (à mettre dans le script de sauvegarde) :

#!/bin/bash

SRC_DIR="/chemin/du/repertoire/source"
DEST_DIR="/chemin/du/repertoire/destination"
STATS_FILE="/chemin/du/fichier/statistiques.xml"

DATE=$(date +%Y-%m-%d)
# Vérifier si le répertoire source existe et est accessible
if [ ! -d "$SRC_DIR" ]; then
    echo "Le répertoire source n'existe pas ou n'est pas accessible."
    exit 1
fi

# Vérifier si le répertoire de destination existe et est accessible
if [ ! -d "$DEST_DIR" ]; then
    echo "Le répertoire de destination n'existe pas ou n'est pas accessible."
    exit 1
fi

#execution sauvegarde et enregistrement dans un fichier temporaire des stats
rsync -avz --stats /chemin/vers/fichier local your_username@adresse_ip_du_serveur::sync_folder --delete --log-file="path/vers/le/logfile" > /tmp/rsync_stats.txt

#vérification du bon déroulement de la sauvegarde stockée dans ?$
if [ $? -eq 0 ]; then
    echo "La sauvegarde s'est déroulée avec succès."
    # Extraire les statistiques pertinentes du fichier temporaire et les formater en XML
    echo "<stats>" > "$STATS_FILE"
    echo "  <client>" >> "$STATS_FILE"
    echo "    <jour>$DATE</jour>" >> "$STATS_FILE"
    awk '/Number of regular files transferred:/ {print "    <nouveaux_fichiers>" $5 "      </nouveaux_fichiers>"}' /tmp/rsync_stats.txt >> "$STATS_FILE"
    awk '/Number of deleted files:/ {print "    <fichiers_supprimes>" $4 "</fichiers_supprimes>"}' /tmp/rsync_stats.txt >> "$STATS_FILE"
    awk '/Number of files transferred:/ {print "    <fichiers_modifies>" $4 "</fichiers_modifies>"}' /tmp/rsync_stats.txt >> "$STATS_FILE"
    awk '/Total file size:/ {print "    <volume_sauvegarde>" $4 "</volume_sauvegarde>"}' /tmp/rsync_stats.txt >> "$STATS_FILE"
    awk '/Total transferred file size:/ {print "    <volume_archives>" $5 "</volume_archives>"}' /tmp/rsync_stats.txt >> "$STATS_FILE"
    echo "  </client>" >> "$STATS_FILE"
    echo "</stats>" >> "$STATS_FILE"

    # Supprimer le fichier temporaire des statistiques
    rm /tmp/rsync_stats.txt
else
    echo "La sauvegarde a échoué avec une erreur."
    exit 1
fi
```
#--delete : supprime les fichiers dans le répertoire de destination qui n'existent plus dans le répertoire source.
#--log-file : spécifie le fichier de journal où les informations de sauvegarde seront enregistrées.