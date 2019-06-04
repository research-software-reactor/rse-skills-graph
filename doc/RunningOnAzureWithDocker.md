
# Deploying the RSE Skills Graph Docker image to Microsoft Azure

This tutorial will describe how to deploy the RSE Skills Graph to the
Azure cloud computing platform via a simple script, provided in the
repository.  We will use the Azure Cloud Shell to deploy to an Azure
Container Instance.

Log in to the [Azure Portal](https://portal.azure.com) and open the
Azure Cloud Shell by clicking on the >_ icon next to the search box at
the top.  Follow the prompts to set up the shell, resource group and
storage if it has not been set up already. Choose "bash" for the
shell.

Clone the RSE Skills Graph git repository into your Azure Cloud Shell
storage.

For non-Manchester folk:
```
git clone https://github.com/research-software-reactor/rse-skills-graph
cd RSESkillsGraph
```
For Manchester RSEs:
```
git clone https://github.com/UoMResearchIT/RSESkillsGraph.git
cd RSESkillsGraph
```

You will be prompted for your GitHub username and password.

Choose a "project" name.  This must be globally unique in Azure, and
consist of lowercase letters and numbers only.  For example
mynamerseskillsgraph.

Run the deployment script:

```
bin/deploy create mynamerseskillsgraph
```

The script takes a few minutes to run, and prints the URL to use for
your new container at the end.  Visit this URL in a browser, and you
should see your own copy of the RSE Skills graph website running on
Azure.

Note that active resources can consume Azure credit, so to take down
everything you just created:

```
bin/deploy delete mynamerseskillsgraph
```
