# Red Hat OpenShift Data Science (RHODS) set up with GPU enablement
Red Hat OpenShift Data Science (RHODS) is built on the robust foundation of Red Hat OpenShift, this cutting-edge solution combines the scalability and flexibility of containerization with the capabilities of machine learning and data analytics. With Red Hat OpenShift Data Science, data scientists and developers can efficiently collaborate, deploy, and manage their models and applications in a secure and streamlined environment.

## Node Feature Discovery installation
Before proceeding with the RHODS installation, lets focus on configuring our node so the GPU is detected. Red Hat’s supported approach is using the NVIDIA GPU Operator, but before installing it, there are a couple of prior requirements we need to accomplish. The first one will be installing the Node Feature Discovery Operator (NFD). This operator will manage the detection of hardware features and configuration in our OpenShift cluster. To do it, we need to go back to the Web Console and select the “**OperatorHub**” section under “**Operators**”. Once there, we need to type *NFD* in the text box and, we will get two results. In my case I will install the operator that is supported by “**Red Hat**”. Click on “**Install**”. This will prompt us with a second page with different configurable parameters. Let’s just keep them by default and press the blue “**Install**” button. 

We can verify the installation by running the following command:
```
watch oc get pods -n openshift-nfd
```
Wait until you see both containers in a *Running* state:
```
NAME                                      READY   STATUS    RESTARTS	  AGE
nfd-controller-manager-6b578bbc6b-cqds5   2/2     Running   0             13d
```

Back to our OpenShift Web Console, we need to create a NFD instance. In the NFD Operator, under Node Feature Discovery, select “**Create instance**” and, as we did before, keep the default values and click “**Create**”. This instance proceeds to label the GPU node.

Again, run this command:
```
watch oc get pods -n openshift-nfd
```
Wait until all the pods are running:
```
NAME                                      READY   STATUS    RESTARTS	  AGE
nfd-controller-manager-6b578bbc6b-cqds5   2/2     Running   0             13d
nfd-master-6f4776454f-gsg9z               1/1     Running   0             14d
nfd-worker-pdbbw                          1/1     Running   0             14d
```

The Node Feature Discovery Operator uses vendor PCI IDs to identify hardware in our node. *0x10de* is the PCI vendor ID that is assigned to NVIDIA, so we can verify if that label is present in our node by running this command: 
```
oc describe node | egrep 'Labels|pci'
```

There, you can spot the *0x10de* present:
```
Labels:             beta.kubernetes.io/arch=amd64
                    cpu-feature.node.kubevirt.io/invpcid=true
                    cpu-feature.node.kubevirt.io/pcid=true
                    feature.node.kubernetes.io/pci-102b.present=true
                    feature.node.kubernetes.io/pci-10de.present=true
                    feature.node.kubernetes.io/pci-14e4.present=true
```

All right! Seems like the Node Feature Operator has been installed correctly, so we can jump into the next step.

## NVIDIA GPU Operator installation

## RHODS installation
Red Hat OpenShift Data Science can be installed from the OpenShift Web Console. Navigate back to the “**Operators**” tab and select “**OperatorHub**”. In the text box now type *RHODS* and select the Red Hat OpenShift Data Science Operator. Click on "**Install**". The defaults will be already configured so we will not need to modify any of them. To start the installation press the blue "**Install**" button. 

