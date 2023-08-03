# Pokedex application deployment

We are going to deploy our Pokedex application to the edge using Podman. In our case, the edge device will be a laptop. Make sure you have installed Podman in your device.

Let's build the container image that will run our model. Create a new folder and navigate into it:
```
mkdir yolov8 && cd yolov8
```
**Inside this folder we need to download our *best.pt* weights obtained after training the model**


Also, I'm going to create a folder to store all the input images:
```
mkdir -p ~/yolov8/inputs
```

Download an example image there:
```
curl -o ~/yolov8/inputs/test.jpg https://raw.githubusercontent.com/rdcolema/tensorflow-image-classification/master/cat.jpg
```

Now, let's define ur *Containerfile* with all the YOLO dependencies:
```
vi Containerfile
```
```
FROM ubuntu:22.04

WORKDIR /yolov8

ADD https://ultralytics.com/assets/Arial.ttf /root/.config/Ultralytics/

COPY best.pt /inputs/pokemon.mp4 /inputs/test.mp4 /yolov8

RUN apt-get update \
    && apt-get install --no-install-recommends -y libgl1-mesa-glx libglib2.0-0 python3 python3-pip \
    && pip3 install ultralytics \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["yolo"]
```

[Optional] Using RHEL as base image:
```
FROM registry.access.redhat.com/ubi9/ubi:latest
#MAINTAINER dialvare "dialvare@redhat.com"

WORKDIR /yolov8

RUN yum update \
    && yum install -y mesa-libGL python3 python3-pip \
    && pip3 install ultralytics \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["yolo"]
```

Build the image:
```
podman build -t yolov8 .
```

It wil take some time, but once finished you can list the images by running this command:
```
podman images
```
```
REPOSITORY                TAG         IMAGE ID      CREATED         SIZE
localhost/yolov8          latest      1cb5c1d869a3  58 minutes ago  7.74 GB
docker.io/library/ubuntu  22.04       5a81c4b8502e  2 weeks ago     80.3 MB
```

Finally, it's time to test our model: 
```
podman run -it --rm -v ~/yolov8:/yolov8 yolov8 detect predict save model=best.pt source=inputs/pokemon.mp4
```

Note: If we embeded our weights and input video in the container image, we can refer those internal files from the container:
```
podman run -it --rm yolov8 detect predict save model=best.pt source=pokemon.mp4
```

# Enable display on Mac
We need to install XQuartz to display graphical interfaces. XQuartz allows cross-platform applications using X11 for the GUI to run on macOS, many of which are not specifically designed for macOS.

Open a Terminal and install the app:
```
brew install xquartz
```

Once completed, open it and enable *'Allow connections from network clients'* under *Security* settings.

Then, enable *X11Forwarding*:
```
sudo vi /etc/ssh/sshd_config
```
```
...
#X11Forwarding yes
...
```
 Finally, configure the display:
```
export DISPLAY='127.0.0.1:0.0'
```

The configuration is ready. It's time to test it:
```
xeyes
```







