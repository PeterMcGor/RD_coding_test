# RD_coding_test
The dicomhandling module can be used:

1- As standalone script calling ```dicomhandling``` from the ```src``` folder.

2- Building and running a docker image locally from the included ```Dockerfile```.

3- Running an image already available in the [DockerHub](https://hub.docker.com/repository/docker/petermcgor/rd_test).

For options 1 and 2, first clone the repository
```
git clone https://github.com/PeterMcGor/RD_coding_test.git
```

For options 1 and 2, open a terminal and change the directory to the cloned repositioty main folder ```RD_coding_test```. 

For option 1: 
- a) Run ```pip install -r requirements.txt``` to install, if necessary, the libraries required by the module.
- b) From your teminal change to the ```src``` folder.
- c) Run ```python3 -m dicomhandling input_folder``` where input folder is the path to the folder containing two DICOM files with the same dimensions. As an example, the repository includes the folder ```T1_3D_TFE - 301``` so you can run as test ```python3 -m dicomhandling ../T1_3D_TFE\ -\ 301/```.

Options 2 and 3 assume that Docker Engine is installed on your system, if it is not you can install it by following the instructions from the official [site](https://docs.docker.com/engine/install/). 

For option 2:
- a) From ```RD_coding_test``` folder run ```docker build -t petermcgor/rd_test``` to build a docker image named ```petermcgor/rd_test``` with the dicomhandling module.
- b) Once the image is built follow the instructions for option 3 from step c).  

For option 3:
- a) There is no need to clone the repository.
- b) Get the already built Docker image from the [DockerHub](https://hub.docker.com/repository/docker/petermcgor/rd_test) running ```docker pull petermcgor/rd_test```.
- c) Run the docker image as interactive with a link to the folder with the DICOM to be processed with ```docker run -it -v /link/to/folder/with/DICOMS/:/data petermcgor/rd_test```, obviously, replace ```/link/to/folder/with/DICOMS/``` with a real path to the data. For example, using the DICOM folder available in the repository and assuming that it is stored at ```/home/user/RD_coding_test/T1_3D_TFE - 301/``` you would need to run ```docker run -it -v /home/user/RD_coding_test/T1_3D_TFE\ -\ 301/:/data petermcgor/rd_test```.
- d) Once the docker image prompt appears run ```python3 -m dicomhandling /data/```.
- e) Run ```exit``` to abandon the docker.
- f) Check the folder with the DICOM files for the ```residues``` folder with the results .
