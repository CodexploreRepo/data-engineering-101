# Terraform

## Introduction

### What is Terraform ?

- [Terraform](https://www.terraform.io/) is an [infrastructure as code](https://www.wikiwand.com/en/Infrastructure_as_code) tool that allows us to provision infrastructure resources as code, thus making it possible to handle infrastructure as an additional software component and take advantage of tools such as version control. It also allows us to bypass the cloud vendor GUIs.
- [Providers](https://registry.terraform.io/browse/providers): code that allows Terraform to communicate to manage resources on
  - AWS
  - Azure
  - GCP
  - Kubernetes
  - Alibaba Cloud

### Why Terraform

- Simplicity in keep track of infrastructure
- Easier collaboration
- Re-producibility
- Ensure resources are removed

### Key Terraform Commands

- `Init` to get the providers I need
- `Plan` what am I about to do
- `Apply` do what is in the tf files
- `Destroy` remove everything defined in the tf files

## Initial Setup

### Terraform (local machine) to GCP via Service Account

#### Service Account

1. Setup a service account for this project and download the JSON authentication key files.

   1. _IAM & Admin_ > _Service accounts_ > _Create service account_
   2. Provide a service account name. We will use `dtc-de-user`. Leave all other fields with the default values. Click on _Create and continue_.
   3. Grant this **service account access to project**: below example is to grant the service account with _Storage Admin_ & _BigQuery Admin_ role
   <p align="center"><img src="../../assets/img/service-account-role-examples.png" width=400/></p>

   4. There is no need to **grant users access** to this service account at the moment. Click on _Done_.
   5. With the service account created, click on the 3 dots below _Actions_ and select _Manage keys_.
   6. _Add key_ > _Create new key_. Select _JSON_ and click _Create_. The files will be downloaded to your computer. Save them to a folder and write down the path.

- :star: Note: This service account `.json` key has to be kept safely as other people can use that for using your account to doing their own stuffs, and it will be billed to your account

##### Method 1: Add Service Account Key to GCP Local Environment Variable

- Create a `keys` folder and provide the service account `.json` key insde.
- Please put the `.gitignore` to remove this key.
- Provide the path to the key to the `GOOGLE_APPLICATION_CREDENTIALS` env variable
  - `GOOGLE_APPLICATION_CREDENTIALS` is an environmental variable used by Google Cloud SDK and various Google Cloud services to specify the path to a key

```Shell
# Method 1: Add for current session only
export GOOGLE_APPLICATION_CREDENTIALS="path_to_file/file.json"


# Method 2: Persist by adding to .bashrc. Use `source ~/.bashrc` or ~/.zshrc to see the change without a restart.
echo export GOOGLE_APPLICATION_CREDENTIALS="path_to_file/file.json" >> ~/.zshrc
```

###### Authentication

- Once the `GOOGLE_APPLICATION_CREDENTIALS` is set with the service account local key path, you can verify with this command: `gcloud auth login`.
  - You'll get a pop up browser and asking you to verify.

```Python
gcloud auth login

# You are now logged in as [investxplore.ai@gmail.com].
# Your current project is [original-gasket-414508].  You can change this setting by running:
#   $ gcloud config set project PROJECT_ID


# Updates are available for some Google Cloud CLI components.  To install them,
# please run:
#   $ gcloud components update
```

##### Method 2 [Most Preferred]: Add Path to Service Account Key in TF's variable

- Unset the `GOOGLE_APPLICATION_CREDENTIALS` if this exists

```shell
unset GOOGLE_APPLICATION_CREDENTIALS
echo $GOOGLE_APPLICATION_CREDENTIALS # return empty
```

- In the `variables.tf`, create the variable `credentials` and provide the path to the key

```yaml
variable "credentials" {
  description = "My Credentials"
  default     = file("./keys/my-creds.json")
  #ex: if you have a directory where this file is called keys with your service account json file
  #saved there as my-creds.json you could use default = "./keys/my-creds.json"
}
```

- In the `main.tf`, provide the `credentials` variable in the `provider`
  - Note: the path should be wrapped by the function `file()`

```yaml
provider "google" {
  # Configuration options
  project = var.project
  region  = var.region
  credentials = file(var.credentials) # the path should be wrapped by the function `file()`
}
```

#### VS Code

- Install "HashiCorp Terraform" extension.

## Terraform Commands

- `terraform fmt` (optional) formats your configuration files so that the format is consistent.
  - Note: this command can be run in the directory that contains `.tf` files to format them.
- `terraform init` initialize your work directory by downloading the necessary providers/plugins and store in `.terraform` folder
