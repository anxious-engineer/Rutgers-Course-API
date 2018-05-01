This library is meant to automate the creation and deployment of lambda functions to the cloud.

### dependencies
Holds all the collective dependencies used for all lambda functions created.

To add to this directory please execute the following from the lambdas directory:
  `pip install <dependency> -t dependencies/`

### deploy
Holds all the deployment packages created from lambdas developed in this library.

### dev
Holds all of the lambda libraries developed for this project.

Each library must atleast have a `lambda_function.py` file, which in turn must contain a `lambda_handler` in order to cover the standard lambda function convention. This method is where aws will start its interaction with the library.

## create_dev_pack
Usage: `./create_dev_pack <path to lambda library>`

Takes the path to a lambda library that needs to be deployed.

First the library and it's dependencies are zipped and placed in the deploy directory, overwriting any of the libraries previous versions.

Then if the lambda already exists in the cloud, it is updated with the new deployment package, otherwise a new lambda is created with the deployment package.

## get_lambda_function_names.py
Helper python script that gets the names of all existing lambda functions.

## NOTE
The scripts used in this library require that the aws cli already be installed and configured for the account that hosts all of the services used.
