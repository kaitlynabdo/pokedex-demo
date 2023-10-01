# Labeling a custom dataset using Label Studio
Label Studio's open-source solution comes containarized. That's why we will need to use OpenShift Virtualization to make it work in our OpenShift node. This instance will allow us to create, run and manage virtual machines and virtualized workloads.

## OpenShift Virtualization installation
It's time to proceed with the Virtualization installation. In our Web Console, we need to navigate to the "**Operators**" tab and select "**OperatorHub**". In the search box type `Virtualization` and the operator we are looking for will appear. Select it and click on "**Install**" on the right side of the screen. The next page will allow us to modify some configuration parameters, but in this case we can proceed with the default ones. Press "**Install**" again and wait until the installation finishes. 

Once completed, we will need to "**Create HyperConverged**" custom resource. Again, we can omit changing any configuration. Finally, click "**Create**" to launch the OpenShift Virtualization installation. Wait until the Status says "**Reconcile completed, Available**".

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
It's time to create the virtual machine where the CVAT application will be deployed. In the "**Virtualization**" page, click on "**Create VM from catalog**". This will forward us to the catalag where all the different VM templates are listed. I will choose the "**CentOS Stream 9**" as the operating system for my VM. When we select it, a pop up window will appear on the right side of the page. Click on "**Customize VirtualMachine**" and complete the following fields:
- **Name**: *labelstudio* (type your preferred name for the VM).
- **Disk source**: *URL (creates PVC)*.
- **Image URL**: *https://cloud.centos.org/centos/9-stream/x86_64/images/CentOS-Stream-GenericCloud-9-20220914.0.x86_64.qcow2*
- **Disk size**: *40 GiB*
- **CLOUD_USER_PASSWORD**: *«vm_password»*
- **CPU | Memory**: *2CPU / 4GiB*

Finally, select "**Create VirtualMachine**" and wait until your virtual machine comes up.

## Label Studio deployment
