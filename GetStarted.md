## Getting started with halte

### Create an environment
Halte is structured to work from a Conda environment. To create the environment, use the Conda prompt to navigate to the project root directory and enter:
`conda env create -f environment.yml`
This will create a Conda environment named `halte`, with all the dependencies installed (provided you have a working internet connection).

### Add the Foundations SDK to enable Atlas
With the environment enabled, navigate to the folder that holds the Atlas installer. Execute the installer with:
`python atlas_ce_installer.py -ia`
to install only the SDK (provided Atlas Server is already installed in another environment)

### Add your data
