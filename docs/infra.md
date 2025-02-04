# Infrastructure configuration
Although our Single Node OpenShift is already installed, there are a couple of pre-requirements we need to meet before proceeding with the Red Hat OpenShift Data Science (RHODS) installation.

## LVM Storage installation
First of all, we will need some kind of storage in our cluster. That's why we will need to install the Logical Volume Manager Storage (LVMS) operator. In the OCP Web Console, navigate to "**Operators**" section on the left-hand menu and click "**OperatorHub**". This will show us the marketplace integrated in OCP with the catalog and the different Operators available. In the search field, type `LVMS`. Once you see the "**LVM Storage**" operator, select it and press "**Install**". We will get to the configuration page. Keep the defaults there and click "**Install**" again. 

![Logical Volume Manager Storage Operator](/docs/images/infra_lvms.png)

Once the installation finishes successfully, we will need to create the Logical Volume Manager Cluster operand. If we go to "**Installed Operators**" in the "**Operators**" tab, we will see a list with all our operators already deployed in our cluster. Select the "**LVM Storage**" operator and then, click "**Create LVMCluster**". This will guide us to the configuration form. Here we can change some of the parameters, like the instance name, device class, etc. We can keep the defaults here too, so we can directly press the ""**Create**" button.

You can track the pods deployment process by running this command on your terminal:
```
watch oc get pods -n openshift-storage
```

We will know that the installation has finished when all the pods' status shows `Running`:
```
NAME                                  READY   STATUS    RESTARTS         AGE
lvms-operator-789d78c76d-8fbsb        3/3     Running   22 (7d13h ago)   39d
topolvm-controller-5496f5d4f4-bd9wd   5/5     Running   36 (7d13h ago)   39d
topolvm-node-gl4qq                    4/4     Running   1 (16d ago)      39d
vg-manager-bwfg6                      1/1     Running   0                39d
```

## Node Feature Discovery installation
Now, let's focus on configuring our node so the GPU can be detected. Red Hat’s supported approach is using the NVIDIA GPU Operator, but before installing it, there are a couple of prior requirements we need to accomplish. The first one will be installing the Node Feature Discovery Operator (NFD). This operator will manage the detection of hardware features and configuration in our OpenShift cluster. To do it, we need to go back to the Web Console and select again the "**OperatorHub**" section under "**Operators**". Once there, we need to type `NFD` in the text box, we will get two results. In my case I will install the operator that is supported by "**Red Hat**". Click on "**Install**". This will prompt us with a second page with different configurable parameters. Let’s just keep them by default and press the blue "**Install**" button. 

![Node Feature Discovery Operator](/docs/images/infra_nfd.png)

Once finished, we need to create a NFD instance. In the "**NFD Operator**", under *Node Feature Discovery*, select "**Create instance**" and, as we did before, keep the default values and click "**Create**". This instance proceeds to label the GPU node.

We can verify the installation by running the following command:
```
watch oc get pods -n openshift-nfd
```

Wait until all the pods are `Running`:
```
NAME                                      READY   STATUS    RESTARTS	  AGE
nfd-controller-manager-6b578bbc6b-cqds5   2/2     Running   0             13d
nfd-master-6f4776454f-gsg9z               1/1     Running   0             14d
nfd-worker-pdbbw                          1/1     Running   0             14d
```

The Node Feature Discovery Operator uses vendor PCI IDs to identify hardware in our node. `0x10de` is the PCI vendor ID that is assigned to NVIDIA, so we can verify if that label is present in our node by running this command: 
```
oc describe node | egrep 'Labels|pci'
```

There, you can spot the `0x10de` tag present:
```
Labels:             beta.kubernetes.io/arch=amd64
                    cpu-feature.node.kubevirt.io/invpcid=true
                    cpu-feature.node.kubevirt.io/pcid=true
                    feature.node.kubernetes.io/pci-102b.present=true
                    feature.node.kubernetes.io/pci-10de.present=true
                    feature.node.kubernetes.io/pci-14e4.present=true
```

All right! The Node Feature Operator has been installed correctly, so we can jump into the next step.

## NVIDIA GPU Operator installation
Now we are ready to install the NVIDIA GPU Operator. Again, navigate to "**OperatorHub**" and type here `NVIDIA`. Select the "**NVIDIA GPU Operator**" and click on "**Install**". Keep the default parameters and click again "**Install**".

![NVIDIA GPU Operator](/docs/images/infra_gpu.png)

Once the Operator is installed, we can proceed with the *ClusterPolicy* creation. To deploy the instance, select the "**NVIDIA GPU Operator**" and click on “**Create instance**” in the *ClusterPolicy* section. Again, keep the default values and click “**Create**”.

While the ClusterPolicy is created, we can see the progress from our terminal by running this command again:
```
watch oc get pods -n nvidia-gpu-operator
```

You will know it has finished when you see an output similar to the following:
```
NAME                                                  READY   STATUS	  RESTARTS   AGE
gpu-feature-discovery-wkzpf                           1/1     Running     0          15d
gpu-operator-76c4c94788-59rfh                         1/1     Running     0          15d
nvidia-container-toolkit-daemonset-5t5dp              1/1     Running     0          15d
nvidia-cuda-validator-m5x4k                           0/1     Completed   0          15d
nvidia-dcgm-8sn57                                     1/1     Running     0          15d
nvidia-dcgm-exporter-hnjc6                            1/1     Running     0          15d
nvidia-device-plugin-daemonset-467zm                  1/1     Running     0          15d
nvidia-device-plugin-validator-bqfr6                  0/1     Completed   0          15d
nvidia-driver-daemonset-412.86.202301061548-0-kpkjp   2/2     Running     0          15d
nvidia-node-status-exporter-6chdx                     1/1     Running     0          15d
nvidia-operator-validator-jj8c4                       1/1     Running     0          15d
```

## Enable Image Registry Operator
On platforms that do not provide shareable object storage, the *OpenShift Image Registry Operator* bootstraps itself as `Removed`. This allows OpenShift to be installed on these platform types. RHODS will require enabling the image registry again in order to be able to deploy the workbenches so we need to enable it again.

First of all, ensure you don't have any running pods in the *openshift-image-registry* namespace:
```
oc get pod -n openshift-image-registry -l docker-registry=default
```

We're good to continue. Now we will need to edit the registry configuration: 
```
oc edit configs.imageregistry.operator.openshift.io
```

Under *storage* include the following lines, making sure you leave the *claim* name blank. This way, the PVC will be created automatically:
```
storage:
  pvc:
    claim:
```

Also, change the *managementState* field from *Removed* to *Managed*:
```
managementState: Managed
```

The PVC will be created as *ReadWriteMany(RWX)*. However, we will need to use *ReadWriteOnce*. The PVC cannot be modified, so we will need to delete the existing one and recreate it modifying the *accessMode*. In the Web Console, go to the "**Storage**" section and select "**PersistentVolumeClaims**". Make sure you have selected the "**Project: openshift-image-registry**" on the top of the page. Then, you will see the "**image-registry-storage**" PVC. Click on the three dots on the right side and select "**Delete PersistentVolumeClaim**". 

Once deleted we can recreate it again. To do so, click on "**Create PersistentVolumeClaim**" and complete the following fields. Then, click "**Create**":
- **StorageClass**: `lvms-vg1`
- **PersistentVolumeClaim name**: `image-registry-storage`
- **AccessMode**: `Single User (RWO)`
- **Size**: `100 GiB`
- **Volume mode**: `Filesystem`

In a few seconds you see the PVC status as `Bound`:

![Image Registry enablement](/docs/images/infra_pvc_bound.png)

With this last step we have completed the installation and configuration of the necessary infrastructure for our project. In the next section we will cover the [Red Hat OpenShift Data Science (RHODS) deployment](https://github.com/dialvare/pokedex-demo/blob/main/docs/rhods.md).

**Next: [Red Hat OpenShift AI (RHOAI) set up](rhods.md)**

