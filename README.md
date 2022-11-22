# rlockerci2
CI for rlocker

This project will show you to install Resource Locker on your Cluster

### Supported platforms:
 - Openshift


### Pre-requirements (The following packages/permissions are required for installing Resource Locker on Openshift):

 - Make sure you have access to your Openshift Cluster, validate by: `oc config get-contexts` check if receiving any output
 - Make sure you have access to instantiate templates in Openshift. 
	- Templates are allowing to create multiple components after receiving a list of environment variables - `oc get template postgresql-persistent -n openshift`
 - `helm cli` is installed. Validate by `helm version`
 - `Python` is installed (3.8 or above). Validate by `python --version`
 - `pip` package manager is installed. Validate by `pip --version`

### Install Resource Locker:
 - Clone the Project by `git clone https://github.com/red-hat-storage/rlockerci.git`
 - Get to the directory of the project from terminal
 - Run `pip install -r requirements.txt` in order to install a single package that supports reading yaml files named **pyyaml** (venv is optional)
 - Create file `settings.yaml` in the root directory of the project - `touch settings.yaml`
	- The following keys are acceptable, please copy and paste this yaml section to `settings.yaml`:
	- `NAMESPACE` Is mandatory
	```
    NAMESPACE: # Decides the name of the namespace to use in the Openshift, specify whether if exists or not exist
    RELEASE_NAME: release-1 # Helm works with release names for its' charts, leave None if you are not sure what it does
    
    POSTGRESQL_USER: admin # Change to the preffered admin name for postgresql authentication, not necessarily need a change
    POSTGRESQL_PASSWORD: admin # Change to the preffered password, it is not recommended having such weak password for db authentication inside your cluster 
    POSTGRESQL_DATABASE: rlocker # No need to change that, that's just the name of the db
    
    DJANGO_CHART_VALUES:
      DJANGO_SECRET: 't4*0k$$8$14a9uk(xtp#_z^5(82&l!uei88c(+91b71@a#8web' # You can always generate a new secret (recommended) from here: https://djecrety.ir/
      DEBUG: False # Debug mode should be false in production, only change if you debug the Django application
      DJANGO_SUPERUSER_USERNAME: admin # Your first user to log in to the Resource Locker website when it is up
      DJANGO_SUPERUSER_PASSWORD: Admin-1 # Your password for the user above, this always could be modified from the Resource Locker instance after deployment (recommended to change to a stronger password)
      DJANGO_SUPERUSER_EMAIL: admin@admin.com # Since the website does not have an SMTP Server with special updates, temporarily, no need to touch that
    
    TAGS:
      QUEUE_SERVICE: queue_service
      DJANGO: latest
      NGINX: rqueue_details_page
	```
 - Run `python run.py`
 - After the deployment, you will receive the status of all the deployed components in the namespace, including the URL for the resource locker!
		