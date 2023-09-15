# Dynamic video file selection front-end
Navigate to the *`frontend`* folder and list the files in the folder:
```
cd frontend/ && ls
```
```
app.py  Containerfile  requirements.txt  static  templates
```
Let's take a look at the Containerfile:
```
vi Containerfile
```
```
#We will use the base image for building the Flask container
FROM registry.access.redhat.com/ubi9/python-311

# It specifies the working directory where the Docker container will run
WORKDIR /app

# Install all the dependencies required to run the Flask application
RUN pip install -r requirements.txt

# Expose the Docker container for the application to run on port 5000
EXPOSE 9000

# Copying all the application files to the working directory
COPY . /app

# The command required to run the Dockerized application
CMD ["python", "/app/app.py"]
```

This Container will use an ubi9 + python image as a base. Then, we will need to install the python requirements. The image will also contain the code present in app.py. Let's take a look at it:
```
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

upload_folder = os.path.join('static', 'uploads')

app.config['UPLOAD'] = upload_folder

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        return render_template('image_render.html', img=img)
    return render_template('image_render.html')


if __name__ == '__main__':
    app.run(debug=True, port=9000)
```

The above code is referencing the *`image_render.html`* file in the *`templates`* folder. Let's review the code:
```
vi ./templates/image_render.html
```
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Rendering Dynamic Images Using Flask</title>
</head>
<body>
<form action="{{ url_for('upload_file') }}" enctype="multipart/form-data" method="POST">
    <input name="img" type="file"/>
    <input type="submit"/>
</form>

{% if img %}
<h1>Rendered Image</h1>
<img src="{{img}}">
{% else %}
<h1>Image will be render here...</h1>
{% endif %}
</body>
</html>
```

It's time to build the front-end image:
```
podman build -t quay.io/dialvare/frontend:latest .
```

Push the image to your repo:
```
podman push quay.io/dialvare/frontend:latest
```

Navigate to the *`x86`* folder:
```
cd x86/ && ls
```
```
apply.sh  delete.sh  deployment_frontend.yaml  deployment_pokedex.yaml  monitor.sh  svc_frontend.yaml  svc_pokedex.yaml
```

Take a look at the object we are going to deploy:
```
vi deployment_frontend.yaml 
```
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: frontend
          image: quay.io/dialvare/frontend:latest
          ports:
            - containerPort: 9000
          securityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop: ["ALL"]
            seccompProfile:
              type: RuntimeDefault
            runAsNonRoot: true
      hostAliases:
        - ip: "127.0.0.1"
          hostnames:
          - "hackfest"
      args:
        - "/etc/hosts"
```

As can be seen, we will deploy the image we have just built. Run the following command to create the resource:
```
oc apply -f deployment_frontend.yaml --insecure-skip-tls-verify=true
```

Once the pod is running, we need to deploy the service:
```
vi svc_frontend.yaml
```
```
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  selector:
    app: frontend
  ports:
    - protocol: TCP
      port: 9000
      targetPort: 9000
      nodePort: 30000   # Specify the desired NodePort value here
  type: NodePort       # Use NodePort type for the service
```

Apply the template:
```
oc apply -f svc_frontend.yaml --insecure-skip-tls-verify=true
```

Check the IP:
```
oc get svc
```
