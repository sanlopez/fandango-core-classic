# FandanGO - core plugin

This is the core plugin of the FandanGO application.

## How to deploy it

1. Create a conda environment and install the needed packages:
   ```
   conda create --name fandango_core_env python=3.12
   conda activate fandango_core_env
   cd fandango-core
   pip install -r requirements.txt
   ```

3. Database setup:

   - [Install MySQL](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/linux-installation.html) database if you do not have it already installed (at localhost or in any machine you can access from the machine FandanGO will run). Make sure the service is running (``systemctl status mysql``)
   
   - Create **fandango_core** database, **fandago** user with a password and grant it access to the database. This could be done as follows from the MySQL shell:
     ```
     CREATE DATABASE fandango_core;
     CREATE USER 'fandango'@'localhost' IDENTIFIED BY 'password';
     GRANT ALL PRIVILEGES ON fandango_core.* TO 'fandango'@'localhost';
     FLUSH PRIVILEGES;
     ```
   
   - Edit the ``config.yaml`` file for setting the password previously provided for **fandango** user (``PASS`` attribute from ``DDBB`` section).
   
   - Create the needed tables by executing ``create_model.py`` script: 
     ```
     conda activate fandango_core_env
     cd fandango-core/db
     python create_model.py
     ```

4. Set other paramenters at ``config.yaml``:

    - ``PATH`` attribute from ``PLUGINS`` section: path where FandanGO plugins are placed.
    - ``ENVS_PATH`` attribute from ``CONDA`` section: path where conda environments are placed. All should be named as fandango_*pluginName*_env


5. Play with FandangGO!💃:
   
   ```
   conda activate fandango_core_env
   cd fandango-core
   python main.py --help
   ```


## Functions currently implemented 

- **createProject**: creates a FandanGO project.

    Examples of call from core's plugin:
    ```
    python main.py --action=createProject
    ```

- **deleteProject**: deletes an existing FandanGO project. Args:
   - projectID [required]: project ID to delete

    Examples of call from core's plugin:
    ```
    python main.py --action=deleteProject --projectId=202401011
    ```

- **copyData**: creates an iRODS collection from data provided. Args: 
   - projectID [required]: project ID given by core's plugin
   - rawData [required]: path of the raw data 

    Example/s of call from core's plugin:
    ```
    python main.py --action=copyData --plugin=irods --projectId=202401011 --rawData=/path/to/data
    ```
