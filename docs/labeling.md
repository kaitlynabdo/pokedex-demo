# Labeling a custom dataset using Label Studio
Label Studio's open-source solution comes containerized. That's why we will need to use OpenShift Virtualization to make it work in our OpenShift node. This instance will allow us to create, run and manage virtual machines and virtualized workloads.

## OpenShift Virtualization installation
It's time to proceed with the Virtualization installation. In our Web Console, we need to navigate to the "**Operators**" tab and select "**OperatorHub**". In the search box type `Virtualization` and select the "**OpenShift Virtualization**" operator. Select it and click on "**Install**" on the right side of the screen. The next page will allow us to modify some configuration parameters, but in this case, we can proceed with the default ones. Press "**Install**" again and wait until the installation finishes. 

![Virtualization configuration](/docs/images/labeling_virt.png)

Once completed, we will need to "**Create HyperConverged**" custom resource. Again, we can omit changing any configuration. Finally, click "**Create**" to launch the OpenShift Virtualization installation. Wait until the *Status* says `Reconcile completed, Available`.

We can verify the installation progress from the terminal window. All OpenShift Virtualization pods will be deployed on the namespace *openshift-cnv*, so we can run this command to check the status:
```
watch oc get pods -n openshift-cnv
```

Once all the pods are up, the output should look similar to this:
```
NAME                                                   READY   STATUS    RESTARTS      AGE
bridge-marker-b2lvf                                    1/1     Running   0             12d
cdi-apiserver-6974f46cf8-cff2s                         1/1     Running   0             12d
cdi-deployment-5bfbb4544c-gx2tb                        1/1     Running   0             12d
cdi-operator-74c7f69c75-vm264                          1/1     Running   0             12d
cdi-uploadproxy-7b8c8854f-fct6n                        1/1     Running   0             12d
cluster-network-addons-operator-6556c66b8-pltks        2/2     Running   0             12d
hco-operator-7b6cbbf469-rfrxh                          1/1     Running   0             12d
hco-webhook-68f44cb446-q6gcw                           1/1     Running   0             12d
hostpath-provisioner-operator-f487576b7-wzshp          1/1     Running   0             12d
hyperconverged-cluster-cli-download-778566579b-mznhp   1/1     Running   0             12d
kube-cni-linux-bridge-plugin-rxnch                     1/1     Running   0             12d
kubemacpool-cert-manager-67457bf487-wsjvd              1/1     Running   0             12d
kubemacpool-mac-controller-manager-6cdcf5df9f-pnghm    2/2     Running   0             12d
kubevirt-plugin-75c7b466c-h5j57                        1/1     Running   0             12d
ssp-operator-78d5984f4d-mbxrm                          1/1     Running   0             12d
tekton-tasks-operator-79c844f459-hpcfs                 1/1     Running   0             12d
virt-api-7c4cc5dc94-lcchc                              1/1     Running   0             12d
virt-controller-7887c7c647-qrk49                       1/1     Running   0             12d
virt-exportproxy-7b5cb679d6-s8tjp                      1/1     Running   0             12d
virt-handler-l5p5l                                     1/1     Running   0             12d
virt-operator-7cd494474-k9sbv                          1/1     Running   0             12d
virt-operator-7cd494474-q9t68                          1/1     Running   0             12d
virt-template-validator-8688f84c96-9msk7               1/1     Running   0             12d
```

Going back to our Web Console, if we reload the page, we can see that a "**Virtualization**" tab has been added to the menu on the left side. 

## Create Virtual Machine
It's time to create the virtual machine where the Label Studio software will be deployed. In the "**Virtualization**" section, select "**VirtualMachines**". Now, click on "**Create VirtualMachine**". This will forward us to the catalog where all the different VM templates are listed. I will choose the "**CentOS Stream 9 VM**" as the operating system for my VM. When we select it, a pop up window will appear on the right side of the page. Click on "**Customize VirtualMachine**" and complete the following fields:
- **Name**: *`centos-labelstudio`* (type your preferred name for the VM).
- **Storage > Disk source**: *`Template default`* (should be already selected as the boot source).
- **Optional parameters > CLOUD_USER_PASSWORD**: *«vm_password»*.
- **Optional parameters > DATA_SOURCE_NAME**: *`centos-stream9`*.
- **Optional parameters > DATA_SOURCE_NAMESPACE**: *`openshift-virtualization-os-images`*.

Click on "**Next**" and then, "**Create VirtualMachine**" and wait until your virtual machine comes up (*Status*: `Running`):

![Virtual Machine](/docs/images/labeling_centos.png)

We can also access the new virtual machine from our terminal. Run the following command to get the virtual machine instance (vmi) name: 
```
oc get vmi
```

This will show you the vmi (`centos-labelstudio` in my case):
```
NAME                 AGE    PHASE     IP             NODENAME                      READY
centos-labelstudio   4d3h   Running   10.128.0.116   r740.pemlab.rdu2.redhat.com   True
```

Use the name displayed above to access the virtual machine from your terminal. You need to log in with your VM credentials (user:`centos` and the `password` you set up during the VM creation):
> **Note**
> If the `virtcl` packages are not installed, you can follow the [Installing virtctl documentation](https://docs.openshift.com/container-platform/4.13/virt/virt-using-the-cli-tools.html#installing-virtctl_virt-using-the-cli-tools). 

```
virtctl console centos-labelstudio
```

## Label Studio deployment
The first steps should be installing and configuring docker:
```
sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf install docker-ce --nobest -y
sudo systemctl enable --now docker
sudo docker login

systemctl is-active docker
systemctl is-enabled docker
sudo docker --version

sudo chmod -R 777 mydata/
sudo usermod -aG docker centos
```

Reboot the VM so that your group membership is re-evaluated. Once the VM comes up again, we can install the Label Studio software on it:
```
docker run -it -p 8080:8080 -v $(pwd)/mydata:/label-studio/data heartexlabs/label-studio:latest
```

Once the installation finishes, we can access the Label Studio graphical interface from a web browser: `http://localhost:8080/`.

## Labeling custom dataset
Once you've accessed the webpage and logged in, we are going to begin labeling our custom dataset. We are going to first create our project by selecting the **Create** button in the top right hand corner. In the **Project Name** tab, you can use whatever name matches your dataset best; in our case, we are just going to name it *pokedex*. Next, we will import the images we want to label in the **Data Import** tab. 

![ezgif com-video-to-gif](https://github.com/kaitlynabdo/pokedex-demo/assets/45447032/1ba1e687-0f1f-4964-9769-34b8990036a9)

In the **Labeling Setup** tab, we are going to select our template we'll use to label our images. Select the **Object Detection with Bounding Boxes**. From there, we will create our labels for our custom data set. Delete the existing labels, type the new labels in the **Add label names** box and add them to the **Labels** list. After that, we'll select **Save** to begin labeling our data. 

![ezgif com-video-to-gif (1)](https://github.com/kaitlynabdo/pokedex-demo/assets/45447032/2f4bd787-20c8-4a1d-919a-c917b3ee759e)

From the project dashboard, we're going to select **Label all tasks**, which will take you to the first image to label. To select a label, you can either click the corresponding label or press the number on your keyboard that corresponds to the label. The Pikachu labeled as 1, you can either press the 1 key on your keyboard or select the label using your cursor. Once you are done labeling, submit them and return to the project dashboard. 

Finally, we'll export our labeled data so we can begin model training. In the top right corner, select **Export**. Since we will use this data to train YOLO object detection models, export the data in the *YOLO* format. 

Now that we have our data, let's head over to our RHODS workbench to get started with model training. 
