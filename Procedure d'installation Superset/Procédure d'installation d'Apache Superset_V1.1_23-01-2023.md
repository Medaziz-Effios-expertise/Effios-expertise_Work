<img src="static_images/Ministry_logo.png" alt="Sorry something unexpected occured!!" style="width:500px;" /> <br>
# **Procédure d'installation d'Apache Superset** <br>
Une démarche accompagnée par <br>
<img src="static_images/logo-effios.png" alt="Sorry something unexpected occured!!" style="width:250px;" /> <br>

| Version | Date | Objet | Statut |
| --- | --- | --- | --- |
| 1.1 | 23/01/2023 |- Ajout de la méthode mise en place du cache<br>- Ajout de la méthode de mise en place du requêtage asynchrone | Diffusable pour expérimentation |
| 1.0 | 14/12/2022 |- Rédaction d'une procédure d'installation d'Apache Superset | Diffusable pour expérimentation |

# Table des matières

- [**Procédure d'installation d'Apache Superset** ](#procédure-dinstallation-dapache-superset-)
- [Table des matières](#table-des-matières)
  - [**Creation of the Superset main user**](#creation-of-the-superset-main-user)
  - [**Mise en place de l'environnement** :](#mise-en-place-de-lenvironnement-)
  - [**Mise en place du backend**](#mise-en-place-du-backend)
    - [**Initialisation de la base de données**](#initialisation-de-la-base-de-données)
  - [**Mise en place du frontend**](#mise-en-place-du-frontend)
  - [**Mise en place du cache**](#mise-en-place-du-cache)
    - [**Installation de Redis**](#installation-de-redis)
  - [**Configuration du système de cache Superset**](#configuration-du-système-de-cache-superset)
  - [**Mise en place du système de requêtage asynchrone**s](#mise-en-place-du-système-de-requêtage-asynchrones)
  - [**Activation de la traduction**](#activation-de-la-traduction)
    - [**Activation de la sélection de la langue**](#activation-de-la-sélection-de-la-langue)
    - [**Mise à jour des fichiers de langue**](#mise-à-jour-des-fichiers-de-langue)
  - [**Lancement de Superset**](#lancement-de-superset)
  - [**Connexion à une base de données externe**](#connexion-à-une-base-de-données-externe)

## **Creation of the Superset main user**
```bash
useradd -m superset 
```

## **Mise en place de l'environnement** :

   Le dépôt git d'Apache Superset est accessible sur le lien suivant : [https://github.com/khansaeffios/superset](https://github.com/khansaeffios/superset)

   Il faut cloner ce dépôt git et ouvrir le dossier superset. La version de Superset à cloner est la version  **2.0.0** :  
   ```bash
   git clone --depth 1 --branch 2.0.0 https://github.com/khansaeffios/superset.git
   ```
   ```bash
   cd superset
   ```
   
L'installation de Superset se fait ensuite en deux temps : l'installation du backend puis celle du frontend.

## **Mise en place du backend**

1. ### **Prérequis du backend**

    L'installation a été réalisée sur un serveur **Ubuntu 22.04**.

    Pour permettre l'installation du backend, des dépendances doivent d'abord être installées en lançant les commandes suivantes qui vont permettre l'utilisation de **MySQL** et de **PostgreSQL**  :
    ```bash
    sudo apt update & sudo apt upgrade
    ```
    ```bash
    sudo apt-get install build-essential libssl-dev libffi-dev python3.9-dev python3.9-pip libsasl2-dev libldap2-dev libmysqlclient-dev
    ```

    Superset fonctionne avec **Python 3.8** ou **3.9** , si vous n'utilisez pas l'une de ces versions, il faut lancer ces commandes :
    ```bash
    sudo add-apt-repository ppa:deadsnakes/ppa
    ```
    ```bash
    sudo apt install python3.9
    ```
2. ### **Installation du backend**

   1. **Créer un environnement virtuel**
   
        ```bash
        sudo apt-get install python3.9-dev python3.9-venv
        ```
        ```bash
        python3.9 -m venv venv
        ```
        ```bash
        source venv/bin/activate
        ```
   2. **Installer les dépendances externes**
       ```bash
       pip install -r requirements/testing.txt
       ```
   3. **Installer Superset en mode éditable**
       ```bash
       pip install -e .
       ```
### **Initialisation de la base de données**

Par défaut, Superset utilise SQLite mais ce n'est pas conseillé pour un environnement de production. Il vaut mieux utiliser MySQL ou PostgreSQL. Voici les étapes à suivre pour mettre en place une base de données PostgreSQL pour Superset :

1. ### **Installer PostgreSQL version 14** (source : [https://computingforgeeks.com/install-postgresql-14-on-ubuntu-jammy-jellyfish/](https://computingforgeeks.com/install-postgresql-14-on-ubuntu-jammy-jellyfish/)) :

   1. **Mise à jour du système et installation des dépendances**
       ```bash
       sudo apt update && sudo apt -y full-upgrade
       ```
       ```bash
       [ -f /var/run/reboot-required ] && sudo reboot -f
       ```
       ```bash
       sudo apt install vim curl wget gpg gnupg2 software-properties-common apt-transport-https lsb-release ca-certificates
       ```
   2. **Ajouter PostgreSQL à Ubuntu**
       ```bash
       apt policy postgresql
       ```
       ```bash
       curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
       ```
       ```bash
       sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb\_release -cs)-pgdg main" \> /etc/apt/sources.list.d/pgdg.list'
       ```
       ```bash
       sudo apt update
       ```
   3. **Installer PostgreSQL**
       ```bash
       sudo apt install postgresql-14
       ```
   4. **Créer une base de données PostgreSQL**

      1. **Se connecter à PostgreSQL**
            ```bash
            sudo -u postgres psql
            ```
      2. **Créer une base de données et un utilisateur pour Superset**
            ```sql
            create database supersetdb;
            ```
            ```sql
            create user superset1 with encrypted password 'Password';
            ```
            ```sql
            grant all privileges on database supersetdb to superset1;
            ```
            ```sql
            \q
            ```
2. ### **Importer la base de données de la PHE dans la base de données PostgreSQL.**

    Nous vous fournissons un dump PostgreSQL avec les données de l'instance de Superset de la PHE qu'il vous faut importer dans la base de données que vous avez créée.
    ```bash
    su – postgres
    ```
    ```sql
    psql supersetdb < superset.dump
    ```
    1. **Mettre à jour la configuration de Superset**

        Dans le dossier **superset/superset** : créer un fichier superset_config.py. Au lieu de modifier le fichier config.py, ce seront les informations ajoutées au fichier superset_config.py qui seront prises en compte.

        Nous vous fournissons le modèle de ce fichier de configuration, veuillez mettre à jour la SECRET_KEY et la base de de données PostgreSQL avec vos informations.

        Pour que les modifications soient prises en compte, il faut définir le chemin vers le fichier de configuration :
        ```bash
        export SUPERSET_CONFIG_PATH=/path/to/your/superset_config.py
        ```
    2. **Initialiser la base de données**
        ```bash
        superset db upgrade
        ```
        _Si vous avez une erreur de type_ _ **ModuleNotFoundError: No module name 'cryptography.hazmat.backends.openssl.x509'** __. Exécutez :_
        ```bash
        pip uninstall cryptography_
        ```
        ```bash
        pip install cryptography==3.4.7_
        ```

    3. **Mettre à jour les rôles et permissions par défaut**
        ```bash
        superset init
        ```
        Une fois ces étapes réalisées, le backend de Superset est mis en place.

## **Mise en place du frontend**

   1. ### **Prérequis du frontend**

      - Node.js version 16
      - npm version 7

      L'utilisation de nvm est conseillée pour réguler l'environnement nodejs :
      ```bash
      curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.0/install.sh | bash
      ```
      ```bash
      cd superset-frontend
      ```
      ```bash
      source ~/.nvm/nvm.sh
      ```
      ```bash
      nvm install 16 --lts
      ```
      ```bash
      nvm use 16
      ```
   2. ### **Installation du frontend**
        Il faut ensuite installer les dépendances du package-lock.json avec :
        ```bash
        npm ci
        ```

        Pour mettre en place le frontend de Superset en production, les assets doivent être construits à l'aide de la commande :
        ```bash
        npm run build
        ```
## **Mise en place du cache**

   Un système de cache est nécessaire sur Superset. Par défaut, sans système de cache configuré Superset, utilise une méthode de cache interne mais il est fortement conseillé d'utiliser un autre outil afin d'optimiser les requêtes.

   Nous allons donc installer **Redis** et configurer Superset à des fins de mise en cache.
### **Installation de Redis**
**Upgrade apt-get :**
```bash
sudo apt-get update
```
```bash
sudo apt-get upgrade
```
**Installer le serveur redis :**
```bash
sudo apt-get install redis-server
```
**Changer le fichier de configuration redis :**
```bash
sudo nano /etc/redis/redis.conf
```
**Ajouter au fichier les lignes suivantes :**
```
#28 MB max memory
maxmemory 128mb
#When mem overflow remove according to LRU algorithm
maxmemory-policy allkeys-lru
```
**Redémarrer et activer redis au redémarrage :**
**Redémarrer redis :**
```bash
sudo systemctl restart redis-server.service
```
**Activer redis au redémarrage :**
```bash
sudo systemctl enable redis-server.service
```
**S'assurer que redis s'affiche dans htop (touche F10 pour sortir de htop) :**
```bash
htop
```
**Pour s'assurer que redis fonctionne il est possible de lancer la commande suivante :**
```bash
redis-cli monitor
```
## **Configuration du système de cache Superset**
Il faut dans un premier temps activer l'environnement virtuel depuis lequel Superset est lancé :
```bash
source superset-env/bin/activate
```
**Installer redis-py :**
```bash
pip install redis
```
## **Mise en place du système de requêtage asynchrone**s

Le fichier de configuration **superset\_config.py** est à mettre à jour avec les configurations permettant l'utilisation de Redis et de Celery. Nous vous fournissons le modèle de ce fichier de configuration mis à jour, veuillez mettre à jour la SECRET\_KEY et la base de de données PostgreSQL.

   Il faut ensuite mettre à jour le fichier **config.py**  :

   - Rechercher la valeur **GLOBAL_ASYNC_QUERIES_JWT_SECRET** et remplacer **test-secret-change-me** par une clé de 32 bytes générée aléatoirement.

   Vous pouvez générer la clé de GLOBAL_ASYNC_QUERIES_JWT_SECRET sur le lien suivant : [https://www.browserling.com/tools/random-bytes](https://www.browserling.com/tools/random-bytes) puis copier / coller la clé générée, par exemple :

![Sorry something unexpected occured!!](static_images/No_idea.png)

Il faut ensuite lancer _celery_, _celery flower_ et _superset_ en parallèle sur trois terminaux différents, depuis l'environnement virtuel de Superset.

**Lancer sur tous ces terminaux (si ce n'est pas déjà fait) :**
```bash
source superset-env/bin/activate
```
**L'étape suivante est d'installer celery flower sur le terminal depuis lequel il sera lancé :**
```bash
pip install flower
```
Pour que les modifications de configuration soient prises en compte, il faut définir le chemin vers le fichier de configuration sur ces trois terminaux (il faut modifier la commande pour mettre le chemin exact vers le fichier superset\_config.py) :
```bash
export SUPERSET_CONFIG_PATH=/path/to/your/superset_config.py
```
**Lancer celery (worker et beat) sur un terminal**
```bash
celery --app=superset.tasks.celery\_app:app worker --pool=prefork -O fair -n worker%i%h & celery --app=superset.tasks.celery\_app:app beat
```
**Lancer flower sur un autre terminal**
```bash
celery --app=superset.tasks.celery\_app:app flower --port=7386
```
**Si vous rencontrer l'erreur :**

Please make sure you give each node a unique nodename using the celery worker `-n` option.
    warnings.warn(DuplicateNodenameWarning(
    **Vous pouvez lancer :**
```bash
ps auxww | grep 'celery\_app' | awk '{print $2}' | xargs kill -9
```
## **Activation de la traduction**
### **Activation de la sélection de la langue**
Ajoutez la variable LANGUAGES à votre superset_config.py. Avoir plus d'une option à l'intérieur ajoutera une liste déroulante de sélection de langue à l'interface utilisateur sur le côté droit de la barre de navigation.
```python
LANGUES = {
    'en' : {'flag' : 'us', 'name' : 'English'},
    'fr' : {'flag' : 'fr', 'name' : 'français'},
}
```
### **Mise à jour des fichiers de langue**
Pour mettre à jour les fichiers de langue, vous devez d'abord se positionner dans le dossier superset, puis lancer cet commande :
```bash
./scripts/babel_update.sh
```
Nous devons convertir le fichier PO en un fichier JSON, et nous avons besoin du téléchargement global du package npm po2json.
```bash
npm installer -g po2json
```
Pour convertir tous les fichiers PO en fichiers JSON formatés, vous pouvez utiliser le script po2json.sh.
```bash
./scripts/po2json.sh
```
Pour que les traductions prennent effet, nous devons compiler les catalogues de traduction dans des fichiers MO binaires.
```bash
pybabel compile -d surensemble/traductions
```
Puis lancer superset sur un terminal différent avec gunicorn comme expliqué par la suite.
## **Lancement de Superset**

**Installation des dépendances :**
```bash
pip install mysqlclient
```
```bash
pip install gevent
```
**Pour lancer Superset, il faut démarrer le serveur ssur le port 8088 avec Gunicorn (en mode Async) avec la commande :**
```bash
gunicorn -w 10 -k gevent --timeout 120 -b 0.0.0.0:8088 --limit-request-line 0 --limit-request-field_size 0 "superset.app:create_app()"
```
## **Connexion à une base de données externe**

1. **Aller dans l'onglet « + » ensuite Data puis « Connect database »** 
![Sorry something unexpected occured!!](static_images/path_to_db.png)

2. **Choisir le type de base de données à connecter (MYSQL par exemple)**
![Sorry something unexpected occured!!](static_images/select_db.png)
  
3. **Renseigner les informations nécessaires**
![Sorry something unexpected occured!!](static_images/edit_db_data.png)
  
4. **Tester la connexion**

<br>
<br>

Source : [https://github.com/apache/superset/blob/master/CONTRIBUTING.md#setup-local-environment-for-development](https://github.com/apache/superset/blob/master/CONTRIBUTING.md#setup-local-environment-for-development)
