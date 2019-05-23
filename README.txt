This is the RSE Skills Graph webapp written in Python 3 with the Flask framework.

To add or update a person's entry modify the JSON entry in people.json. People with spaces in their surname should use underscore e.g. Le_Blanc.
It will be displayed properly with a space. The "interests" for each person need to come from Wikipedia main entries - that is our controlled vocabulary.


requirements.txt should contain the Python modules needed.
You also need to install the C based GraphViz code. On my Mac I did: brew install graphviz

To run locally: python application.py
(where python must be Python 3)

TODO: tried to push to Azure Cloud but need for GraphViz installation preventing this currently.
This https://github.com/matthew-brett/pygraphviz-wheels might help.
