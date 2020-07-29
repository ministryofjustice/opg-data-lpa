# Terraform in Opg-Data-Template

The purpose of this readme is to clarify what the terraform code is doing and how it interacts
with the CI pipeline as well as giving some common commands and tasks anyone can perform with the
right permissions

### Workspace based environments

This repository uses workspaces. Workspaces allow you modify a terraform state file through applying
and destroying configuration independently of other workspaces. For example if I was in workspace 'X'
and locked the state file by killing off an apply half way through then although no one could work on
workspace 'X', workspace 'Y' would be completely unaffected.

We use this principal so that in our dev environments we create workspaces based on our branch name.
As such we can have multiple copies of an environment in the same AWS account.

The workspaces are controlled by the variable TF_WORKSPACE. If you wish manually run a plan or apply against
one of your branch workspaces for development purposes then you must be in the
```terraform/environment``` folder.
You would then run the following replacing myworkspace with your workspace name:
```export TF_WORKSPACE=myworkspace```.
Next run your terraform command (aws vault profile could be different depending how you set it up):
```aws-vault exec identity -- terraform plan```.

The ```terraform/account``` folder is run once per account rather than being branch based.

### OpenApi orientated rest API (and tests)

The API gateway is generated from the OpenApi spec stored in the opg-data repository. We pull this in at
run time via the circleci job. In your local environment this is pulled in if you don't have any versions
of it in your base repo folder via .envrc. This follows the pattern used across a lot of OPG of using direnv
(https://direnv.net/).

If you want to build with the latest versions locally then remove all local copies of the OpenApi spec from
the base directory and type ```direnv allow``` and it will pull in all the open api versions from opg-data.

The OpenApi spec controls the auth method, validation and the versioning by means of using stage variables to point
to separate lambdas.

### API Gateway deployment

The way the amazon API Gateway product works is that we have a rest api that has integrations to end points.
In our case these are lambdas. To access the gateway a stage needs to be deployed and a DNS entry can then
point to a particular stage.

Our deployments in this lambda are controlled by one of 3 variables being updated.

1) stage_version: If there's a new API version released
2) content_api_sha: If the content of the openapi spec changes
3) lambda_version_folder_sha: If the pre-generated sha of the lambda folder changes
(e.g there's been a change in the lambda code).

If any of these change it triggers a 'deployment'.

### Release a new version

Stages point to the relevant version of the lambda for the stage using stage variables. These are defined in
the OpenApi spec and assigned by the terraform code.

The process for releasing a new version is:

1) Make sure there's a new OpenApi spec with a different version number.
We should have as many OpenApi specs as we want to support. If we still want to keep them
afterwards but have retired the version from terraform then they should be moved to an
archive folder in opg-data
2) Copy previous v* folder in lambda_functions and incrememnt by one. Make all necessary lambda
changes to work with the new specification.
3) In lambda.tf in ```terraform/environment```, copy the lambda code for previous version and
add new modules with appropriate variables passed in.
4) In locals.tf update the ```latest_openapi_version``` variable.
5) In ```stage.tf``` copy and paste the module deploy_v* and add new module for this version.

This will allow us to connect to two separate end points based on stage version.

It is not practical using this method, to support long term, multiple versions as deployments are per
Rest API. As such the deployment and old stage crystallised in time and cannot be modified once new version is released.
The lambdas are completely separate so a bug fix on the lambda side could be done on a previous version.

### Lambdas

Lambdas are controlled through modules as per above.

### Lambda layers

Lambda layers contain all the requirements for a lambda. Whilst it would be nice to use a sha for
the full folder this was causing both the lambda and layer to deploy on each deploy.
As such it is part of the CI pipeline to check the sha of the requirements.txt.
There is a comment in there where you can update the date which will change the sha and thus update
the layer. Also if a new requirement is added it will rebuild the layer. Otherwise it will stick with
the current layer.

### Issues

There are a couple of issues with the policy that force us to use openapi spec policy which means we can't specify
the individual gateway arn. This seems fine as policy is per gateway only and we can lock it down to resources:

- https://github.com/terraform-providers/terraform-provider-aws/issues/5364
- https://github.com/terraform-providers/terraform-provider-aws/pull/13619
