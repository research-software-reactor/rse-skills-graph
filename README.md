
# Leeds RSE adaptation of the RSE Skills graph
This is a fork of the RSE Skills graph web app adapted for the Research Computing Team at Leeds.

> # This is the RSE Skills Graph web app written in Python 3 with the Flask framework
>Original code by Steve Pettifer; mods by Ian Cottam, Colin Morris, Ian Hinder;
> The University of Manchester;
>Apache 2 Licence
>
>To add or update a person's entry modify the JSON entry in >people.json. People with spaces in their surname should use >underscore e.g. Le_Blanc.
It will be displayed properly with a space. The "interests" for each person need to come from Wikipedia main entries - that is our controlled vocabulary.
>
>requirements.txt should contain the Python modules needed.
You also need to install the C based GraphViz code. On my Mac I did: brew install graphviz
>
>To run locally: python application.py
(where python must be Python 3)
>
>We have this running on Azure now as a Docker container (needed because of mix of Python and C libraries).
>
>
>Any kind of relationships can be built and displayed using this software.
>The JSON is fairly obvious. There are two levels, called "interests" and "technologies", because of the initial use here:
>http://supervisors.cs.man.ac.uk.
>Interests are clickable, but technologies not. (Some browsers let you right-click a technology and look up its definition.)
>In the RSE-skills application we really just use Interests, so everything is clickable. We do use technologies sparingly as commentary.
>
>Portrait images of people can be included in an images directory, but we don't use that faclity in RSE-skills.
>
>## Possible other applications that have been suggested:
>- UK wide RSE skills
>- Microsoft Student Partner skills
>
>
>If you want general self-service ability to modify entries, a web front-end would be nice.
>For a fairly closed, trusted community you can use Git to let people access and change people.json directly.
>
>
>- To run in Docker, see [Running in Docker](doc/RunningInDocker.md)
>
>- To run in Docker on Microsoft Azure, see [Running in Docker on Azure](doc/RunningOnAzureWithDocker.md)
