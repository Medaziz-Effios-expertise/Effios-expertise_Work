# Procédure de mise à jour des traductions d'Apache Superset

1. Créez un environnement virtuel et activez-le : 
   
    ASSUREZ QUE PYTHON 3.8 ou 3.9 EST INSTALLÉ

    Pour windows : https://www.python.org/downloads/windows/

    Pour Mac : https://www.python.org/downloads/mac-osx/
    
    Allez sous le répertoire source : 
    ``` 
    cd Main-pathway/superset
    ``` 
    créer un environnement virtuel et l'activer :
    ``` 
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Assurez-vous d'abord que les dépendances nécessaires sont installées :
    ```
    pip install -r superset/translations/requirements.txt
    ```

3. Extraction de nouvelles chaînes à traduire et generation du fichier .pot :
 
   Lorsque de nouvelles chaînes sont ajoutées à l'application, elles doivent être extraites et ajoutées au fichier de modèle de traduction superset/translations/messages.pot. Pour mettre à jour le fichier de modèle superset/translations/messages.pot avec les chaînes d'application actuelles, exécutez la commande suivante :
    ```
    pybabel extract -F superset/translations/babel.cfg -o superset/translations/messages.pot -k _ -k __ -k t -k tn -k tct .
    ```

4. Mise à jour des fichiers de langue .po :
    ```
    pybabel update -i superset/translations/messages.pot -d superset/translations --ignore-obsolete
    ```

5. Modifier les traductions fr dans le fichier .po sous le chemin:
    ```
    superset/superset/translations/fr/LC_MESSAGES/messages.po
    ``` 
    via l'outil POEdit :          
        https://poedit.net/download
   
    Pour effectuer la traduction sur MacOS, vous pouvez installer poedit via Homebrew :
    ```
    brew install poedit
    ```

7. Installez po2json :
    ```
    cd superset-frontend
    npm install po2json
    ```
8. Convertir les fichiers PO en fichiers JSON, vous pouvez utiliser :
	 ```
    superset-frontend/node_modules/.bin/po2json --domain superset --format jed1.x superset/translations/fr/LC_MESSAGES/messages.po superset/translations/fr/LC_MESSAGES/messages.json
    ```
9. Formatez les fichiers JSON avec Prettier : 
    ```
    superset-frontend/node_modules/.bin/prettier --write superset/translations/fr/LC_MESSAGES/messages.json
    ```
10. Pour que les traductions prennent effet, nous devons les compiler en fichiers MO binaires :
    ```
    pybabel compile -d superset/translations
    ```
Documentation de référence : <a href="https://superset.apache.org/docs/contributing/translations">Lien pour les documentations de traduction</a>


