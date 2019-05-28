
# Deploying the RSE Skills Graph Docker image to Microsoft Azure

Prerequisites:

- A working Azure account
- A command line Azure client, either local or through the Azure Portal
- The RSESkillsGraph repository cloned from Git and built as a local Docker image, as described in [Running in Docker](RunningInDocker)

These instructions use the command line, but the same can be achieved through the web portal user interface.

If using the CLI tool on your local machine, first log in to azure:

```
az login
```

## Resource group

Create a Resource Group, which is used to track accounting information:

```
az group create --name rseSkillsGraph-rg --location westeurope
```

The other resources you create will be created in this resource group.

## Container registry

Create a Container Registry in the resource group.

- Note: container registry names must be globally unique across all of Azure, so for this example, use a prefix such as your initials (here "ich").  They also can only contain letters and numbers.  There also seems to be an authentication requirement later that it is all lowercase.

```
az acr create --resource-group rseSkillsGraph-rg --name ichrseskillsgraphcr --sku Basic --admin-enabled true
```

Take note of the loginServer in the output, e.g. 

  "loginServer": "ichrseskillsgraphcr.azurecr.io"

Show the admin password:

```
az acr credential show --resource-group rseSkillsGraph-rg --name ichrseskillsgraphcr --query "passwords[0].value"
```

Take a note of the password, e.g. RUXXXXXY62ERN2MFZVK4Z=DRolu47Lx7Y.

- Note: this is not a good practice; the password will later end up stored in your shell history.  However, the alternative (setting up Service Principals and key stores) is quite involved, and it did not appear to work with the free account.

## Push the Docker image

Log in to the container registry.

```
az acr login --name ichrseskillsgraphcr
```

Ensure you are in the RSESkillsGraph git checkout directory, and tag the existing docker image with a tag referencing the new registry, based on the tag you built it with:

```
docker tag rseskillsgraph:latest ichrseskillsgraphcr.azurecr.io/rseskillsgraph:latest
```

Push the image you built earlier up to the new registry:

```
docker push ichrseskillsgraphcr.azurecr.io/rseskillsgraph:latest
```

## Container

Finally, create the container.

- Note that the DNS name of the container must also be globally unique across all of Azure, so again, prefix it with a unique string (here "ich")
- Ensure that the registry password in the command below is the same as the password noted above

```
az container create \
    --name rseskillsgraph \
    --resource-group rseSkillsGraph-rg \
    --image ichrseskillsgraphcr.azurecr.io/rseskillsgraph:latest \
    --registry-login-server ichrseskillsgraphcr.azurecr.io \
    --registry-username ichrseskillsgraphcr \
    --registry-password "RUXXXXXY62ERN2MFZVK4Z=DRolu47Lx7Y" \
    --dns-name-label ich-rseskillsgraph \
    --query ipAddress.fqdn \
    --ports 5000
```

Take note of the full DNS name in the output, for example ```ich-rseskillsgraph.westeurope.azurecontainer.io```.  The RSE Skills graph should now be available on the web at

  http://ich-rseskillsgraph.westeurope.azurecontainer.io:5000

where the DNS name should be that returned by the ```az container create``` command.  It might take a while before the container is up and running and the page loads.

## Closing it down

Note that active resources can consume Azure credit, so to take down everything you just created:

```
az container delete --name rseskillsgraph --resource-group rseSkillsGraph-rg
az acr delete --name ichRSESkillsGraphCR
az group delete --name rseSkillsGraph-rg
```


