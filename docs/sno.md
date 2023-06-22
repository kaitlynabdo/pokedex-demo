# Single Node OpenShift installation using the Assisted Installer on baremetal
Single Node OpenShift is Red Hat’s solution for edge use cases when we want to run OpenShift workloads on constrained and remote locations, where, typically the physical space for systems decreases and our network may be restricted by No or intermittent connectivity. The minimum system requirements for SNO will just be 4 cores and 16 GB of RAM. SNO is capable of offering control and worker node capabilities in a single server, reducing the footprint and provides users with a consistent experience across the sites where OpenShift is present. It can be deployed using standard installation methods on bare metal hosts and certified hypervisors. Lastly, be aware that the major tradeoff with an installation on a single node is the lack of high availability.

In this demo we will use the Assisted Installer provided with the Hybrid Cloud Console to deploy Single Node OpenShift on real bare metal hardware, equipped with a GPU, in my case, an NVIDIA Tesla M60 GPU Card.

## Assisted Installer
As a starting point, let’s navigate to the [OpenShift Red Hat Hybrid Cloud Console](https://console.redhat.com/openshift). There, we will need to log in using our Red Hat account credentials. Once on the landing page, we are going to click on “**Create Cluster**” so we can start with the Assisted Installer. In this case, we are going to use a real bare metal host, so we will need to select the “**Datacenter**” tab. Here, under the Assisted Installer section, let’s click on “**Create Cluster**”. This will guide us to the cluster configuration wizard page. 

### Cluster details
As you can see there are plenty of fields that we can configure in our cluster:
- **Cluster name**: *pokedex* (insert any preferred name)
- **Base domain**: *pemlab.rdu2.redhat.com* (to match our environment domain).
- **OpenShift version**: *OpenShift 4.13.2* (latest version at the time I'm writting this).
- **CPU architecture**: *x86_64* (our bare metal host uses Intel architecture).
- Check the “**Install single node OpenShift (SNO)**” box.

Finally, let's leave the rest of the parameters as default and click on the blue “**Next**” button until you reach the *Host Discovery* section.
> **Note**
> We are skipping the *Operators* section, as the idea of this demo is to show the full process of installing the LVMS and the OpenShift Virtualization operator. But, feel free to check both options in case you want to speed up the process.

### Host discovery
In the Host discovery page, we can see that the installer is waiting for a host. To do so, firstly we need to create it by clicking on “**Add host**”. This will show us a pop-up window. The purpose of this step is to generate a discovery ISO to boot the node and install OpenShift there. Here, we can see different options. In our case we want to boot using virtual media, so we need to select “**Minimal image file**”. Note that if we are going to use this option, our node will require internet access to provision the image.

The next step is to provide our “**SSH public key**” so we can connect to the host machine. As you probably know, we can get it using our Terminal by running the following command. Copy and paste it into the wizard:
```
cat ~/.ssh/id_rsa.pub”
```
At this point, we are good to “**Generate the Discovery ISO**”. Instantly, we will be ready to download the generated image. Click on “**Download Discovery ISO**” to have store it in your laptop. This will start the download process that shouldn't take too long, but it will depend on your internet connection.

### Node configuration
Now, we will need to switch to our bare metal node. Here we need to configure our node to boot using our discovery iso. Depending on the host, this procedure could be slightly different in your case, but overall, the steps would be pretty similar to these ones:

In our case, we will click on “**Connect Virtual Media**”. There, we will be able to “**Choose the File**” with the discovery iso we just downloaded. Now we are good to “**Map the device**”. Also we will need to configure our host to boot using the virtual media. We will click on “**Boot**” and select “**Virtual CD/DVD/ISO**” from the list. 

Finally, all we need to do is reboot the system. Click on “**Power Off System**” and then “**Power On the System**” again. With this, the SNO host provisioning will begin. 

Once finished and back to the OpenShift Red Hat Hybrid Cloud Console, we will be able to see our machine automatically recognised and listed in the *Host Inventory* section. Make sure to check the “Status” displayed is “**Ready**”. If so, we can directly jump to the end of the process and proceed with the SNO installation.

### SNO installation
The installer will complete automatically all the steps needed to have our node up and running. We can track this process through this progress bar. It should take some time to finish the installation.

## Accessing the SNO
Once the installation has finished, we can access the OpenShift node using the credentials provided under the Installation bar. You should be able to spot the URL to the Web console, the kubeadmin user and the password that we will use to authenticate. Click on "**Open Console**”. You will probably see a warning message complaining about the security of the page, but we can safely ignore it. Once on the logging page, we will use the credentials provided after the SNO installation. By this, finally we successfully logged into the Single Node OpenShift Web Console!

Most of the steps during this demo will be executed from the Web Console. Nevertheless, it’s always useful having a Terminal window connected to our SNO so we can double check everything is created correctly. To get the token, click on our current user “**kube:admin**” in the upper right corner and select “**Copy logging command**”. This will open a new tab in our web browser. If we click on “**Display token**”, we can copy the first command shown and paste it into our terminal. Now run the following command to ensure everything is setled correctly:
```
oc get node
```
The output should look similar to this:
```
NAME                          STATUS   ROLES                         AGE   VERSION
r740.pemlab.rdu2.redhat.com   Ready    control-plane,master,worker   14d   v1.25.4+77bec7a
```

## Namespace creation
Before continuing, let's create a namespace where all the resources tailored to this demo will be deployed. The follwoing command will create the new project. Name it as you prefer; I'll choose *pokedex* for this demo:
```
oc new-project pokedex
```

Remember also to select this project from the Project drop-down menu at the top left in the Web Console, when deploying the resources for our demo. 

## [Optional] Set up Identity Provider
Instead of using the *kubeadmin* user, we can set up new users and give them the needed permissions. For this porupose we are going to configure an *htpasswd* identity provider. First of all, using the terminal, we will need to create the file that will contain the users and their passwords encrypted:
```
htpasswd -c -B -b ~/htpasswd user1 <password>
```

In case we need to add other users, the command will be quite similar to the previous one:
```
htpasswd -B -b ~/htpasswd user2 <password>
```

Now we can define the secret cointaining our users credentials:
```
oc create secret generic htpass-secret --from-file=htpasswd=~/htpasswd -n openshift-config 
```

Finally, modify the oauth to add the identity provider:
```
oc edit oauth cluster 
```

Add these lines:
```
...
spec:
  identityProviders:
  - htpasswd:
      fileData:
        name: htpass-secret
    mappingMethod: claim
    name: Pokedex
    type: HTPasswd
```




