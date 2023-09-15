# Pokedex application deployment using Podman
We are going to use a RHEL 9.2 Virtual Machine where we are going to simulate an x86 edge device deployment. 
Create a new Virtual Machine and install RHEL 9.2 there. You can get the RHEL 9.2 Boot iso (x86) image from the [Red Hat Developer page](https://developers.redhat.com/products/rhel/download#rhel-new-product-download-list-61451). 

## Configuring MicroShift
Now it's time to install MicroShift. We just need to follow the official documentation available in the [Product page](https://access.redhat.com/documentation/en-us/red_hat_build_of_microshift/4.13/html/installing/microshift-install-rpm). 

In our case, we also had to extend the volume group to get some *VFree* space. This was the process we followed: 
```
sudo lsblk
```
```
sudo pvcreate /dev/sdb
```
```
sudo vgextend rhel_ibm-p8-kvm-03-guest-02 /dev/sdb
```

Now we can proceed with the MicroShift installation. To get the right *rpm* packages we need to enable two repositories: 
```
sudo subscription-manager repos \
--enable rhocp-4.13-for-rhel-9-$(uname -m)-rpms \
--enable fast-datapath-for-rhel-9-$(uname -m)-rpms
```

Install MicroShift from there: 
```
sudo dnf install -y microshift
```

Download your installation pull secret from the [Red Hat Hybrid Cloud Console](https://console.redhat.com/openshift/install/pull-secret). We will use it to authenticate with the container registries that we will be using. Then, copy the file to the */etc/crio* folder and give it the right permissions:
```
sudo cp $HOME/openshift-pull-secret /etc/crio/openshift-pull-secret
```
```
sudo chown root:root /etc/crio/openshift-pull-secret
```
```
sudo chmod 600 /etc/crio/openshift-pull-secret
```

It's time to start the MicroShift service:
```
sudo systemctl start microshift
```

Copy the kubeconfig file to the right folder adn give it the permissions needed:
```
mkdir -p ~/.kube/
```
```
sudo cat /var/lib/microshift/resources/kubeadmin/kubeconfig > ~/.kube/config
```
```
chmod go-r ~/.kube/config
```
And finally, we can connect to our MicroShift instance. We should see the following list with the pods Running:
```
NAMESPACE                  NAME                                       READY   STATUS    RESTARTS        AGE
kube-system                csi-snapshot-controller-5875fd4f9d-mtgdh   1/1     Running   2               28h
kube-system                csi-snapshot-webhook-5c969d4577-5pvm5      1/1     Running   2               28h
openshift-dns              dns-default-vrgsh                          2/2     Running   4               28h
openshift-dns              node-resolver-pb7j8                        1/1     Running   2               28h
openshift-ingress          router-default-df4b59b87-x9c5j             1/1     Running   7 (110m ago)    28h
openshift-ovn-kubernetes   ovnkube-master-xx8lr                       4/4     Running   9               28h
openshift-ovn-kubernetes   ovnkube-node-hsnj7                         1/1     Running   3               28h
openshift-service-ca       service-ca-5f584b7d75-7drlv                1/1     Running   2               28h
openshift-storage          topolvm-controller-5fccfdf45c-cf9g7        5/5     Running   79 (76m ago)    28h
openshift-storage          topolvm-node-xkxsh                         4/4     Running   18 (108m ago)   28h
```

## Building the image
Navigate to the *`container`* folder: 
```
cd container/ && ls
```
```
Containerfile		pokemon.mp4		redhat.py_websocket
best.pt			redhat.py		templates
```

Before continuing, let's take a look to the Containerfile:
```
vi Containerfile
```
```
# Use an official Python runtime as the base image
FROM registry.access.redhat.com/ubi9/python-311

# Set the working directory in the container
WORKDIR /app

# Copy the code into the container
COPY . /app

USER root
RUN dnf install -y libpng

# Install Python dependencies
RUN pip install opencv-python-headless Pillow numpy flask flask_socketio eventlet gevent gevent-websocket
RUN git clone https://github.com/ultralytics/yolov5 && cd yolov5 && sed -i s/'opencv-python>'/'opencv-python-headless>'/g requirements.txt && pip install -r requirements.txt && pip uninstall -y opencv-python && pip install --force-reinstall opencv-python-headless

# Expose the port if needed
EXPOSE 5000

ENV LD_LIBRARY_PATH=/usr/lib64:/usr/lib64/openmpi/lib/:$LD_LIBRARY_PATH

USER 1001

# Run the script when the container launches
CMD ["python3", "redhat.py"]
```

