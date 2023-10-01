# Red Hat OpenShift Data Science (RHODS) set up
Red Hat OpenShift Data Science (RHODS) combines the scalability and flexibility of containerization with the capabilities of machine learning and data analytics. With Red Hat OpenShift Data Science, data scientists and developers can efficiently collaborate, deploy, and manage their models and applications in a secure and streamlined environment.

## RHODS installation
Red Hat OpenShift Data Science can be installed from the OpenShift Web Console. Navigate back to the "**Operators**" tab and select "**OperatorHub**". In the text box now type `RHODS` and select the "**Red Hat OpenShift Data Science**" operator and click on "**Install**". The defaults will be already configured so we will not need to modify any of them: 

![RHODS installation](/docs/images/rhods_config.png)

To start the installation press again the blue "**Install**" button. Once the status is `Succeeded`, the deployment has finished successfully.

## Create Data Science Project
To access the RHODS Web Console, we can get it from the OCP Console. In the right side of the top bar, you will find an "**square icon**" formed by 9 smaller squares. Clik on it and select "**Red Hat OpenShift Data Science**":

![RHODS console](/docs/images/rhods_console.png)

A new window will open. Log in again using your OpenShift credentials (kubeadmin or your identity provider user).
> **Note**
> If you are hitting a networking issue, that could mean that you need to add the url to the `/etc/hosts` file as we did with the OpenShift routes during the SNO installation.

## Project set up
Once we are logged, in the landing page we will see a layout similar to the one we have in the OpenShift Web Console. In the left-handed menu, navigate to the "**Data Science Projects**" tab. Next, click "**Create data science project**" and type your preferred project names; in our case `pokedex`. Then press "**Create**". 

## Create Workbech


