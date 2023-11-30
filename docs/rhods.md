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
Once we are logged, in the landing page we will see a layout similar to the one we have in the OpenShift Web Console. In the left-handed menu, navigate to the "**Data Science Projects**" tab. Next, click "**Create data science project**". Type your preferred project names; in our case `pokedex` and press "**Create**". This is the namespace where all the resources tailored to this demo will be deployed.

## Create Workbench
Inside our project select "**Create workbench**". This will guide us to the workbench configuration page. Complete the fields to match the following:
- **Name**: *`pokedex`* (insert any preferred name).
- **Image selection**: *`PyTorch`*.
- **Version selection**: *`2023.1`* (Recommended).
- **Container size**: *`Medium`* (this will depend on your node resources; the more, the better).
- **Number of GPUs**: *`2`* (in this case, our node has 2 NVIDIA GPU cards). If this field is not enabled, skip this part, complete the workbench creation and then check the [Optional] section at the end of this chapter.
- [X] Check the "**Create new persistent storage**" box.
  -   **Name**: *`pokedex`* (insert any preferred name).
  -   **Persistent storage size**: *`100 GiB`* (we can always extend it later if needed).
     
Once completed the form, please click on "**Create workbench**". You should have something similar to this image:

![RHODS project](/docs/images/rhods_project.png)

That's it! Now you can access the Workbench Interface clicking on "**Open**" and log in using your credentials. At this point, we are ready to start with the dataset preparation for training the AI model, but we will cover it in the next chapter: [Labeling a custom dataset using Label Studio](https://github.com/dialvare/pokedex-demo/blob/main/docs/labeling.md).
> **Note**
> It is likely you will need to add the url to the `/etc/hosts` file as we did before with the RHODS console.

### [Optional] GPU drop-down menu enablement
Sometimes the drop-down does not show or is greyed out. It's a known bug, but don't worry! We can enable it using the next trick:
1. Turn off the Workbench and wait until the *Status* shows `Stopped`.
2. Back in the OpenShift Web Console navigate to *Administration* > *CustomResourceDefinitions* and search `Dashboardconfig`.
3. Select the `OdhDashboardConfig` custom resource definition. Then click on the *Instances* tab and `odh-dashboard-config` next.
4. In the *YAML* tab, add the following line (note that the number entered will the maximum value shown in the dropdown):
   ```
   notebookController:
    enabled: true
    gpuSetting: '2'
    notebookNamespace: rhods-notebooks
    pvcSize: 20Gi
   ```
6. Save the changes and wait a couple of minutes.
7. Navigate back to the RHODS console, click on the three dots on the right side of the workbench name and select *Edit workbench*.
8. The *Number of GPUs* menu should be enabled now. Select how many you want to use (2 in my case). Click *Update workbench*.
9. Turn on the workbench again and wait until the *Status* shows `Running`.

**Next: [YOLOv5 training on a custom dataset on Red Hat OpenShift Data Science (RHODS)](training.md)**



