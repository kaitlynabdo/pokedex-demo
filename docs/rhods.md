# Red Hat OpenShift Data Science (RHODS) set up with GPU enablement
Red Hat OpenShift Data Science (RHODS) is built on the robust foundation of Red Hat OpenShift, this cutting-edge solution combines the scalability and flexibility of containerization with the capabilities of machine learning and data analytics. With Red Hat OpenShift Data Science, data scientists and developers can efficiently collaborate, deploy, and manage their models and applications in a secure and streamlined environment.

## RHODS installation
Red Hat OpenShift Data Science can be installed from the OpenShift Web Console. Navigate back to the “**Operators**” tab and select “**OperatorHub**”. In the text box now type *RHODS* and select the Red Hat OpenShift Data Science Operator. Click on "**Install**". The defaults will be already configured so we will not need to modify any of them. To start the installation press the blue "**Install**" button. 

Track the installation process by running this command:
```
watch oc get pods -n redhat-ods-operator
```
Once the status is *Ready*, the deployment has finished sucessfully.

## Create Data Science Project

