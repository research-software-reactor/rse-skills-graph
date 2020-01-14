from __future__ import print_function
from flask import Flask, render_template, request, redirect, url_for

import json
import pygraphviz as pgv
import re
from lxml import etree
#replace StringIO
import io
#from io import BytesIO
#from io import StringIO
import urllib
#import urllib2
import urllib.request
import urllib3
import string
import sys
import os
import os.path
import natsort
from collections import OrderedDict


app = Flask(__name__)

os.environ['PATH'] = os.environ['PATH'] + ':/usr/local/bin'
os.environ['GV_FILE_PATH'] = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/images/')) + '/'

print('PATH: ' + os.environ['PATH'], file=sys.stderr)
print('GV_FILE_PATH: ' + os.environ['GV_FILE_PATH'], file=sys.stderr)

def get_people():
    filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'people.json'))
    return get_file_contents(filepath)

# thanks to Colin Morris for adding this code originally
def get_skills_list():
    skills_list = {}
    json_results = get_people()
    for supervisor, data in json_results.items():
        for section in data:
            # add if block to prevent emails being added to skills list
            if section != "email":
                for item in json_results[str(supervisor)][section]:
                    if item not in skills_list:
                        skills_list[item] = 1;
                    else:
                        skills_list[item] = skills_list[item] +1;

    skills_list_new = OrderedDict(natsort.natsorted(skills_list.items()))
    return skills_list_new


def get_file_contents(filename):
    data = None

    try:
        fp = open(filename, 'rb')
        try:
            contents = fp.read()
            data = json.loads(contents)
        finally:
            fp.close()
    except IOError:
        print('Could not open JSON file:' + filename, file=sys.stderr)
        sys.exit(1)

    return data

def get_titles(topic):
    url = 'https://en.wikipedia.org/w/api.php'
    values = {
        'action' : 'query',
        'list' : 'search',
        'srwhat' : 'text',
        'srsearch' : topic.encode('utf8'),
        'format' : 'json',
        'srlimit' : '40'
    }

    ## Big urllib change for Python 3 below...
    #data = urllib.urlencode(values) # Python 2
    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8') # necessary for python 3

    request = urllib.request.Request(url, data)
    #response = urllib2.urlopen(request) # Python 3 version below
    response = urllib.request.urlopen(request)
    json_response = response.read()
    json_result = json.loads(json_response)

    try:
        results = []
        for result in json_result['query']['search']:
            results.append(result['title'])
    except:
        results = []
        print("ERROR: no title found for topic: " + topic.encode('utf8'))

    return results

def get_graph_string(graph):
    #output = StringIO.StringIO()
    output = io.BytesIO()
    graph.draw(output, format = 'svg')
    svg = output.getvalue()
    output.close()

    svg_parser = etree.XMLParser()
    svg_obj = etree.fromstring(svg, svg_parser)

    svg_obj.attrib['width'] = '100%'
    del svg_obj.attrib['height']

    images = svg_obj.findall('.//{http://www.w3.org/2000/svg}image')

    # Convert all image href links to match server
    # For example, anonymous.png becomes static/images/anonymous.png
    # Have to do this because graphviz doesn't allow you to specify the
    # URL to an image, only the file path.
    for image in images:
        image_filename = image.attrib['{http://www.w3.org/1999/xlink}href']
        image_url = url_for('static', filename = 'images/' + image_filename)
        image.attrib['{http://www.w3.org/1999/xlink}href'] = image_url

    return etree.tostring(svg_obj, pretty_print = True).decode('utf-8')

def get_image_files():
    image_files = []
    image_dir = os.environ['GV_FILE_PATH']

    for root, sub_folders, files in os.walk(image_dir):
        for filename in files:
            actual_file_name = os.path.join(root, filename)
            if filename.endswith('.png'):
                image_files.append(filename)

    return image_files

def build_graph(name, results, topics):
    graph = pgv.AGraph(overlap = 'false', name = name)
    people = get_people()

    for person in results:
        forename, surname = person.lower().split()

        image_file = 'anonymous.png'
        image_files = get_image_files()

        for filename in image_files:
			#newstr = starturlsource[index+len(pattern):index+len(pattern)+17]
            if str.find(filename, surname) != -1 and str.find(filename, forename) != -1:
                image_file = '%s' % (filename)

        # check added for _ in name e.g. Anja Le_Blanc; that is: convert _ to space
        myperson= person.replace(' ', '\n')
        graph.add_node(person, label = myperson.replace('_' , ' '),
                       fontname = 'Helvetica',fixedsize = True,
                       imagescale = True, width = '1.5', height = '1.5',
                       fontcolor = 'white', shape = 'circle', style = 'filled',
                       color = '#303030',
                       URL = "mailto:"+people[person]['email'][0],
                       image = image_file)

        interests = people[person]['interests']
        for interest in interests:
            if interest in topics:
                color = '#A02020FF'
                shape = 'ellipse'
            else:
                color = '#105060EE'
                shape = 'ellipse'

            label = re.sub('\(.*\)', '', interest)

            graph.add_node(interest, label = label, style = 'filled',
                           fontname = 'Helvetica', shape = shape, color = color,
                           fontcolor = 'white',
                           URL = url_for('show_topic', name = interest)
                           )

            graph.add_edge(person, interest, color = '#00000050')

        if 'technologies' in people[person]:
            for technology in people[person]['technologies']:
                if technology in topics:
                    color = '#B01050FF'
                    shape = 'ellipse'
                else:
                    color = '#701050EE'
                    shape = 'ellipse'

                label = re.sub('\(.*\)', '', technology)

                graph.add_node(technology, label = label, style = 'filled',
                               fontname = 'Helvetica', shape = shape,
                               color = color, fontcolor = 'white')

                graph.add_edge(person, technology, color = '#00000050')

    graph.layout(prog = 'neato')

    return graph

@app.route('/')
def index():
    graph_name = 'UoL Research Software Engineers and their skills'

    results = set()
    topics = []

    people = get_people()

    for person in people:
        results.add(person)

    graph = build_graph(graph_name, results, topics)
    graph_str = get_graph_string(graph)
    interests_links = get_interests_links()
    return render_template('graph.html', name=graph_name,
                           node_count=len(graph.nodes()),
                           graph=graph_str,
                           interests=interests_links)


def get_interests_links():
    interests_skills = get_skills_list()
    interests_links = ""
    index_link = url_for('index')
    for skill, count in interests_skills.items():
        interests_links += '<a href="' + index_link + 'topic/' + str(skill) + \
        '" title="' + str(count) + ' records">' + str(skill) + '</a><br>'
    return interests_links


@app.route('/person/<name>')
@app.route('/person/')
@app.route('/person')
def show_person(name=None):
    if not name:
        interests_links = get_interests_links()
        return render_template('notfound.html', interests=interests_links)

    graph_name = name.replace('_', ' ') + "'s skills"

    results = set()
    topics = []

    results.add(name)

    graph = build_graph(graph_name, results, topics)
    if graph is False:
        pname=name
        interests_links = get_interests_links()
        return render_template('notfound.html',
                               search_term=pname,
                               interests=interests_links)

    graph_str = get_graph_string(graph)

    return render_template('graph.html',
                           name=graph_name,
                           node_count=len(graph.nodes()),
                           graph=graph_str)


@app.route('/topic/<name>')
def show_topic(name):
    main_topic = name
    graph_name = 'UoL RSEs and their skills related to ' + name

    results = set()
    topics = get_titles(name)

    people = get_people()
    interests_links = get_interests_links()

    for person in people:
        for topic in topics:
            if topic in people[person]['interests']:
                results.add(person)

        if 'technologies' in people[person]:
            for topic in topics:
                if topic in people[person]['technologies']:
                    results.add(person)

    graph = build_graph(graph_name, results, topics)
    graph_str = get_graph_string(graph)
    return render_template('graph.html', name=graph_name,
                           node_count=len(graph.nodes()),
                           graph=graph_str, interests=interests_links)

# 2019-04-08 | New : Try to handle empty search
@app.route('/topic/')
def show_topic_notfound():
    interests_links = get_interests_links()
    return render_template('notfound.html', interests=interests_links)

@app.route('/topic-search')
def topic_search():
    topic = request.args.get('topic')
    return redirect(url_for('show_topic', name = topic))


if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')
