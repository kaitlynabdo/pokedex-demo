# YOLOv5 training on a custom dataset on OpenShift AI
Now that our RHODS environment is set up and our data has been prepared, we can begin model training and make some predictions. We will head back to the RHODS Dashboard to view our Data Science Projects. We'll start by opening the pokedex workbench. 

<img width="1736" alt="Screenshot 2023-11-30 at 9 36 48 AM" src="https://github.com/kaitlynabdo/pokedex-demo/assets/45447032/85e7d75f-1c96-4426-b009-74eeae752565"><br>

Log with your cluster credentials and you will be promted to allow permissions, keep everything checked and click allow selected permissions. 

<img width="897" alt="Screenshot 2023-11-30 at 9 41 43 AM" src="https://github.com/kaitlynabdo/pokedex-demo/assets/45447032/91a615b8-a54f-4f4a-a249-f92e1151cd71"><br>

Now we're in our Jupyter environment, where we will be doing all experimentation, training and testing. First we will need to import our [Pokedex repository](https://github.com/OpenShiftDemos/pokedex-demo) from GitHub. First click the icon featured below.

<img width="550" alt="Screenshot 2023-11-30 at 9 39 31 AM" src="https://github.com/kaitlynabdo/pokedex-demo/assets/45447032/13abc41d-dba7-40b0-ac8b-3cb7df8dcf8f"><br>

From there, you click *Clone a repository* and paste the [Pokedex repository](https://github.com/OpenShiftDemos/pokedex-demo) to clone it in your Jupyter environment.

<img width="471" alt="Screenshot 2023-11-30 at 9 40 22 AM" src="https://github.com/kaitlynabdo/pokedex-demo/assets/45447032/3e32b9a8-6e5b-4996-b159-2d6a2cb0e25d"><br>

After a few moments, you should see the *pokedex-demo* directory in your environment. Under *pokedex-demo/Notebooks/*, open *Pokedex_YOLO_v8_new.ipynb* and follow the notebook for further instructions. 
