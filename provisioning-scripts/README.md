# Scripts for Provisioning and Managing Nectar Virtual Machines

## Pre-requisites

1) Set Nectar Cloud Key & Secret
To run any of the scripts in this folder, you will first need to set your Nectar keys (EC2 Key and Secret) as an
environment variable. This is important as we cannot have this sensitive information over our public git repository

To get your access key and secret, follow the steps below:
+ login to nector cloud at: https://dashboard.rc.nectar.org.au/project/
+ Navigate to "Access & Security" from the left-sidebar
+ At the top, navigate to "API Access"
+ Then select the "View Credentials" from the top-left buttons
+ Copy the EC2 Access Key and Secret safely somewhere (NEVER share this over public internet as anyone can
        access our machines using these credentials

Once you have the key and secret, you need to set it as your environment variables:

If you are using Ubuntu, just run the following commands on your terminal
```bash
export ENV_KEY='your_ec2_key'
export ENV_SECRET='your_ec2_secret'
```

These two commands will set your environment variables but will only be valid for that terminal session.
You can add these two commands in your `~/.bashrc` file if you want them to be loaded everytime the terminal
opens up


2) Set Route53 Key & Secret
We are using Route53 to manage our DNS entry. We purchased a domain name for this project: `cloudprojectnectar.co`. We
are managing all out instances using domain names for the sake of simplicity and also for management of instances, in
case we want to swap instances without the users feeling any difference.

To set the keys, run the following commands:
```bash
export AWS_ENV_KEY='AKIAIMMBKKRHGSD7NHQA'
export AWS_ENV_SECRET='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'
```

NOTE: We are providing these credentials for the examiner to check our work. The keys will be deleted after grading is
done.

3) Run Services
