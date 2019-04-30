import boto3
import requests
import time
import json
import thread
from requests_aws4auth import AWS4Auth

default_repo_name = "tvlk-repo"


###
# get ec2 iam keys
###
def ec2_auth():
  role = requests.get("http://169.254.169.254/latest/meta-data/iam/security-credentials/").text
  role = requests.get("http://169.254.169.254/latest/meta-data/iam/security-credentials/"+role)
  return AWS4Auth(role.json()["AccessKeyId"], role.json()["SecretAccessKey"], "ap-southeast-1", 'es', session_token=role.json()["Token"])


###
# Basic elasticsearch call
###
def create_repo(host,bucket,role,repo_name):
  url = host + "_snapshot/" + repo_name
  payload = {
    "type": "s3",
    "settings": {
      "bucket": bucket,
      "region":"ap-southeast-1",
      "role_arn": role
      }
    }
  payload = json.dumps(payload)
  r = requests.put(url, auth=ec2_auth(), data=payload, headers={"Content-Type": "application/json"})
  return r

def create_snapshot(host,repo_name,snapshot_name):
  print("creating snapshot with name : " + snapshot_name)
  url = host + "_snapshot/" + repo_name + "/" + snapshot_name
  payload = '{}'
  r = requests.put(url, auth=ec2_auth(), data=payload, headers={"Content-Type": "application/json"})
  return r

def restore(host,repo_name,snapshot_name):
  url = host + "_snapshot/" + repo_name + "/" + snapshot_name + "/_restore"
  payload = '{}'  
  r = requests.post(url, auth=ec2_auth(), headers={"Content-Type": "application/json"})
  return r

def get_repo(host):
  url = host + "_snapshot/_all"
  r = requests.get(url, auth=ec2_auth(), headers={"Content-Type": "application/json"})
  return r

def get_repo_detail(host,repo_name):
  url = host + "_snapshot/" + repo_name + "/_all"
  r = requests.get(url, auth=ec2_auth(), headers={"Content-Type": "application/json"})
  return r

def delete_repo(host,repo_name):
  url = host + "_snapshot/" + repo_name
  r = requests.delete(url, auth=ec2_auth(), headers={"Content-Type": "application/json"})
  return r

def get_aliases(host):
  url = host + "_aliases"
  r = requests.get(url, auth=ec2_auth(), headers={"Content-Type": "application/json"})
  return r

def get_indices(host):
  url = host + "_cat/indices"
  r = requests.get(url, auth=ec2_auth(), headers={"Content-Type": "application/json"})
  return r

def delete_index(host,index):
  url = host +index
  r = requests.delete(url, auth=ec2_auth(), headers={"Content-Type": "application/json"})
  return r

def get_index_detail(host,index):
  url = host + index
  r = requests.get(url, auth=ec2_auth(), headers={"Content-Type": "application/json"})
  return r

def search(host,target):
  url = host + target +"/_search"
  r = requests.get(url, auth=ec2_auth(), headers={"Content-Type": "application/json"})
  return r

def adv_search(host,target):
  url = host + target
  r = requests.get(url, auth=ec2_auth(), headers={"Content-Type": "application/json"})
  return r

###
# job wrapper
###

def get_snapshot_status_from_list_snapshots(json,snapshot_name):
  for i in range(5):
    print "try "+ str(i) + " " + snapshot_name
    for x in json["snapshots"]:
      if x["snapshot"]==snapshot_name:
        return x
  return

def snapshot_checker_worker(identifier,host,snapshot_name):
  while get_snapshot_status_from_list_snapshots(get_repo_detail(host,default_repo_name).json(),snapshot_name)["state"] == "IN_PROGRESS":
    print "Snapshoting on "+identifier+" "+get_snapshot_status_from_list_snapshots(get_repo_detail(host,default_repo_name).json(),snapshot_name)["state"]
    time.sleep(5)
    pass
  print "Snapshoting on "+host+" finished with status "+get_snapshot_status_from_list_snapshots(get_repo_detail(host,default_repo_name).json(),snapshot_name)["state"]
  pass

def initiate_snapshot_async(tuples,s3,role):
  for identifier, host in tuples.items():
    create_repo(host,s3,role,default_repo_name)
    time.sleep(5)
    localtime = time.localtime()
    time_string = time.strftime("%Y-%m-%d-%H-%M-%S", localtime)
    snapshot_name = identifier+"-"+time_string
    try:
      create_snapshot(host,default_repo_name,snapshot_name)
      time.sleep(5)
      thread.start_new_thread( snapshot_checker_worker, (identifier, host, snapshot_name) )
    except:
      print "Error: unable to start snapshot or thread on "+ identifier
      pass
    pass
  return

def initiate_snapshot(tuples,s3,role):
  for identifier, host in tuples.items():
    create_repo(host,s3,role,default_repo_name)
    time.sleep(2)
    localtime = time.localtime()
    time_string = time.strftime("%Y-%m-%d-%H-%M-%S", localtime)
    snapshot_name = identifier+"-"+time_string
    try:
      create_snapshot(host,default_repo_name,snapshot_name)
      time.sleep(2)
      snapshot_checker_worker(identifier, host, snapshot_name)
    except:
      print "Error: unable to start snapshot or thread on "+ identifier
      pass
    pass
  return

def get_latest_snapshot(json,identifier):
  ret = None
  for x in json["snapshots"]:
    if x["snapshot"].startswith(identifier):
      if ret == None:
        ret = x
      elif x["start_time_in_millis"] > ret["start_time_in_millis"]:
        ret = x
      pass
    pass
  return ret


def initiate_restore(tuples,s3,role):
  for identifier, host in tuples.items():
    create_repo(host,s3,role,default_repo_name)
    time.sleep(2)
    json = get_repo_detail(host,default_repo_name).json()
    snapshot_name = get_latest_snapshot(json,identifier)["snapshot"]
    if snapshot_name == None:
      continue
    print "Restoring "+snapshot_name+" for " + identifier
    restore(host,default_repo_name,snapshot_name)
    print get_indices(host).text
    pass
  return
