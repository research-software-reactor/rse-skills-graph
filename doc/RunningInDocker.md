
# Running the RSE Skills Graph using Docker

First, install Docker if it is not already installed.  The direct download links are available in the release notes:

- Mac OS: https://hub.docker.com/editions/community/docker-ce-desktop-mac
- Windows: https://hub.docker.com/editions/community/docker-ce-desktop-windows
- Linux: Instructions are available for several distros at https://docs.docker.com/install/ under *Linux* on the sidebar

Check Docker is working from the command line with

```
docker run hello-world
```

Clone the RSESkillsGraph repo:

For Manchester RSEs:
```
git clone git@github.com:UoMResearchIT/RSESkillsGraph.git
```

For non-Manchester folk:
```
git clone https://github.com/research-software-reactor/rse-skills-graph
```

Build the Docker image; this will take a couple of minutes.  The image is built according to the Dockerfile in the root of the repository.

```
cd RSESkillsGraph
docker build -t rseskillsgraph:latest .
```

This gives the new image the tag "rseskillsgraph:latest" for later reference.

Run the image as a new container:

```
docker run -p 5000:5000 rseskillsgraph:latest
```

This maps port 5000 on your machine to port 5000 in the container.  Connect to http://localhost:5000 in a browser.

You should see the RSE Skills graph.

