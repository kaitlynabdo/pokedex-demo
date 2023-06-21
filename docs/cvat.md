# Deploy the Computer Vision Annotation Tool (CVAT) on OpenShift Virtualization
Now that we’ve got our Single Node OpenShift ready, we are good to install the OpenShift Virtualization Operator. This instance will allow us to create, run and manage virtual machines and virtualized workloads. The [Computer Vision Annotation Tool (CVAT)](https://github.com/opencv/cvat) is still not kubernetes compatible, but it is containerized. That's why we will need to use OpenShift Virtualization to make it work in our OpenShift node.

## LVM Storage installation

## OpenShift Virtualization installation
To proceed with the installation, in our Web Console, we need to navigate to the “**Operators**” tab and select “**OperatorHub**”. This will show us the marketplace integrated in OCP with the catalog and the different Operators availables. In the search box type *Virtualization* and the operator we are looking for will appear. Select it and click on “**Install**” on the right side of the screen. The next page will allow us to modify some configuration parameters, but in this case we can proceed with the default ones. Press “**Install**” again and wait until the installation finishes. 

Once completed, we will need to “**Create HyperConverged**” custom resource. Again, we can omit changing any configuration. Finally, click “**Create**” to launch the OpenShift Virtualization installation. Wait until the Status says “**Reconcile completed, Available**”.

We can verify the installation progress from the terminal window. All OpenShift Virtualization pods will be deployed on the namespace *openshift-cnv*, so we can run this command to check the status:
```
watch oc get pods -n openshift-cnv
```
Once all the pods are up the output should look similar to this:
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

Going back to our Web Console, if we reload the page, we can see that a “**Virtualization**” tab has been added to the menu on the left side. 

## Create Virtual Machine
It's time to create the virtual machine where the CVAT application will be deployed. In the "**Virtualization**" page, click on "**Create VM from catalog**". This will forward us to the catalag where all the different VM templates are listed. I will choose the "**CentOS Stream 9**" as the operating system for my VM. When we select it, a pop up window will appear on the right side of the page. Click on "**Customize VirtualMachine**" and complete the following fields:
- **Name**: *cvat* (type your preferred name for the VM).
- **Disk source**: *URL (creates PVC)*.
- **Image URL**: *https://cloud.centos.org/centos/9-stream/x86_64/images/CentOS-Stream-GenericCloud-9-20220914.0.x86_64.qcow2*
- **Disk size**: *40 GiB*
- **CLOUD_USER_PASSWORD**: *«vm_password»*
- **CPU | Memory**: *2CPU / 4GiB*

Finally, select "**Create VirtualMachine**" and wait until your virtual machine comes up.

## CVAT deployment
We can access the new virtual machine from our terminal. Run the following command to get the virtual machine instance (vmi) name: 
```
oc get vmi
```
This will show you the vmi (*cvat* in my case):
```
NAME   AGE    PHASE     IP             NODENAME                      READY
cvat   4d3h   Running   10.128.0.116   r740.pemlab.rdu2.redhat.com   True
```
Use the name displayed above to access the virtual machine from your terminal:
```
virtcl console cvat
```
The first steps should be for installing and configuring docker:
```
sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf install docker-ce --nobest -y
sudo systemctl enable --now docker
sudo docker login

systemctl is-active docker
systemctl is-enabled docker
sudo docker --version

sudo usermod -aG docker centos
```

Reboot the VM so that your group membership is re-evaluated. Once the machine is running again, its time to install composer:
```
curl -L https://github.com/docker/compose/releases/download/2.18.1/docker-compose-`uname -s`-`uname -m` -o docker-compose
sudo mv docker-compose /usr/local/bin && sudo chmod +x /usr/local/bin/docker-compose

docker compose version
```

Now we can clone the CVAT repository:
```
sudo dnf install git -y
git clone https://github.com/opencv/cvat
cd cvat
```

At this point, we can start configuring the application. To do so, you will need to export the host domain (*.apps.pokedex.pemlab.rdu2.redhat.com*, in my case):
```
export CVAT_HOST=.apps.pokedex.pemlab.rdu2.redhat.com
printenv | grep CVAT_HOST
```

Now we can spin up the containers:
```
sudo docker compose up -d
sudo docker ps
```
The output will look similar to this:
```
CONTAINER ID   IMAGE                                      COMMAND                  CREATED      STATUS      PORTS                                                                                          NAMES
b9ee01617316   cvat/ui:dev                                "/docker-entrypoint.…"   4 days ago   Up 4 days   80/tcp                                                                                         cvat_ui
5c4cda1e5a3f   timberio/vector:0.26.0-alpine              "/usr/local/bin/vect…"   4 days ago   Up 4 days                                                                                                  cvat_vector
25dd3b2bd1d2   cvat/server:dev                            "/usr/bin/supervisor…"   4 days ago   Up 4 days   8080/tcp                                                                                       cvat_worker_annotation
66518c5b0c98   cvat/server:dev                            "/usr/bin/supervisor…"   4 days ago   Up 4 days   8080/tcp                                                                                       cvat_utils
a5900cf62070   cvat/server:dev                            "/home/django/backen…"   4 days ago   Up 4 days   8080/tcp                                                                                       cvat_server
73d18957814b   cvat/server:dev                            "/usr/bin/supervisor…"   4 days ago   Up 4 days   8080/tcp                                                                                       cvat_worker_export
b8228fbfa0a3   cvat/server:dev                            "/usr/bin/supervisor…"   4 days ago   Up 4 days   8080/tcp                                                                                       cvat_worker_webhooks
41c06733506f   cvat/server:dev                            "/usr/bin/supervisor…"   4 days ago   Up 4 days   8080/tcp                                                                                       cvat_worker_import
8d4e8e7b38d5   cvat/server:dev                            "/usr/bin/supervisor…"   4 days ago   Up 4 days   8080/tcp                                                                                       cvat_worker_quality_reports
71e53575f48d   clickhouse/clickhouse-server:22.3-alpine   "/entrypoint.sh"         4 days ago   Up 4 days   8123/tcp, 9000/tcp, 9009/tcp                                                                   cvat_clickhouse
4534846a3a47   traefik:v2.9                               "/entrypoint.sh --pr…"   4 days ago   Up 4 days   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp, 80/tcp, 0.0.0.0:8090->8090/tcp, :::8090->8090/tcp   traefik
fecc5095c783   postgres:15-alpine                         "docker-entrypoint.s…"   4 days ago   Up 4 days   5432/tcp                                                                                       cvat_db
6a70ec29d41f   openpolicyagent/opa:0.45.0-rootless        "/opa run --server -…"   4 days ago   Up 4 days                                                                                                  cvat_opa
5ac17ed8f705   redis:7.0-alpine                           "docker-entrypoint.s…"   4 days ago   Up 4 days   6379/tcp                                                                                       cvat_redis
```

Next will be creating a superuser to manage groups and users. The following command will prompt some configuration steps:
```
sudo docker exec -it cvat_server bash -ic 'python3 ~/manage.py createsuperuser'
```

If everything is correct, we should be able to check if the CVAT web site is responding:
```
curl localhost:8080
```
Here will appear our application:
```
        <meta
            name="description"
            content="Computer Vision Annotation Tool (CVAT) is a free, open source, web-based image and video annotation tool which is used for labeling data for computer vision algorithms. CVAT supports the primary tasks of supervised machine learning: object detection, image classification, and image segmentation. CVAT allows users to annotate data for each of these cases"
        />
        <meta name="”robots”" content="index, follow" />
        <title>Computer Vision Annotation Tool</title>
```

Awesome! The final step will be exposing the URL, so we can access it. Exit the VM shell and run these commands:
```
virtctl expose vmi cvat --port=8080 --name=cvat
oc create route edge --service=cvat
oc get route cvat
```
Here we can see our URL:
```
NAME   HOST/PORT                                          PATH   SERVICES   PORT    TERMINATION   WILDCARD
cvat   cvat-pokedex.apps.pokedex.pemlab.rdu2.redhat.com          cvat       <all>   edge          None
```

Copy and paste it in your Web Browser to access the admin page: [https://cvat-pokedex.apps.pokedex.pemlab.rdu2.redhat.com/admin/](https://cvat-pokedex.apps.pokedex.pemlab.rdu2.redhat.com/admin/)


