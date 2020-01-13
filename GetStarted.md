## Getting started with halte

### Create a Python environment
Halte is structured to work from a Conda environment. To create the environment, use the Conda prompt to navigate to the project root directory and enter:
`conda env create -f environment.yml`
This will create a Conda environment named `halte`, with all the dependencies installed (provided you have a working internet connection).

### Add the Foundations SDK to enable Atlas
With the environment enabled, navigate to the folder that holds the Atlas installer. Execute the installer with:
`python atlas_ce_installer.py -ia`
to install only the Foundations SDK (provided Atlas Server is already installed in another environment).

### Create a custom Docker image for Atlas to run

On a terminal, navigate to the `.docker` directory and execute:

```
docker build . -t halte:latest
```

In Foundations' `job.config.yaml` file, update the worker with:
```
worker:
  image: halte:latest
```

### Add your data

- Mount data address into docker image through `job.config.yaml`:
```
worker:
  (...)
  volumes:
    /c/users/vbfal/projects/halte-data:
      bind: /data
      mode: rw
```
