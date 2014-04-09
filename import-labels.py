#!/usr/bin/python
#
# This script will take the labels from one GitHub repository's
# Issues and sync all of your other repos' Issues with them. After
# running, all of your repos will have the exact same set of Issue
# labels. It assumes that every repo has Issues enabled.
#
# REQUIREMENTS: needs the 'requests' library, available from pip
#
# Config variables:
#   source_repo_name:   the repository that has the labels you want copied
#   username/password:  your personal GitHub credentials
#   company:            Set this if you're doing it for an Organization.
#                       Leave blank if just for your personal account.
 
### CONFIG
source_repo_name = 'test'
username = 'ojharavi'
password = 'GetSetGo@72'
company = ''
####
 
import json
import requests
 
api = "https://api.github.com/"
credentials = (username, password)
 
if company:
    owner = company
    repos_raw = requests.get(api+"orgs/"+company+"/repos",
                             auth=credentials,
                             params={"type":"owner"})
else:
    owner = username
    repos_raw = requests.get(api+"user/repos",
                             auth=credentials,
                             params={"type":"owner"})
repos = repos_raw.json()
desired_labels = []
 
def main():
    exclude_source_repo()
    set_desired_labels()
    print_desired_labels()
    delete_old_labels()
    add_desired_labels_to_repos()
 
def exclude_source_repo():
    for index, repo in enumerate(repos):
        if repo['name'] == source_repo_name:
            repos.pop(index)
 
def set_desired_labels():
    desired_labels[:] = [{"name": label['name'],
                          "color": label['color']} for label in get_labels_for(source_repo_name)]
 
def get_labels_for(repo_name):
    labels_raw = requests.get(api+"repos/"+owner+"/"+repo_name+"/labels", auth=credentials)
    return labels_raw.json()
 
def print_desired_labels():
    print "Using this label set from {0}:".format(source_repo_name)
    print '\n'.join([label['name'] for label in desired_labels])
 
def delete_old_labels():
    for repo in repos:
        name = repo['name']
        print "Deleting labels from {0} repo".format(name)
        for label in get_labels_for(name):
            url = label['url']
            requests.delete(url, auth=credentials)
 
def add_desired_labels_to_repos():
    for repo in repos:
        name = repo['name']
        print "Adding new labels to {0} repo".format(name)
        for label in desired_labels:
            requests.post(api+"repos/"+owner+"/"+name+"/labels",
                          auth=credentials,
                          data=json.dumps(label))
 
if __name__ == "__main__":
    main()
