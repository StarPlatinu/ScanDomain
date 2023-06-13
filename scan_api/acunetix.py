#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import requests
import urllib3
import time
'''
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

or 

pip install requests[security]
'''
requests.packages.urllib3.disable_warnings()

tarurl = "https://localhost:13443"
apikey="1986ad8c0a5b3df4d7028d5f3c06e936c92499d7a2551486ca068b2153922f287"
headers = {"X-Auth":apikey,"content-type": "application/json"}

def addtask(url=''):
    #add task
    data = {"address":url,"description":url,"criticality":"10"}
    try:
        response = requests.post(tarurl+"/api/v1/targets",data=json.dumps(data),headers=headers,timeout=30,verify=False)
        result = json.loads(response.content)
        return result['target_id']
    except Exception as e:
        print(str(e))
        return

def startscan(url):
    # Get all tasks first. Avoid duplication
    # Add task to get target_id
    # start scanning
    '''
    11111111-1111-1111-1111-111111111112    High Risk Vulnerabilities          
    11111111-1111-1111-1111-111111111115    Weak Passwords        
    11111111-1111-1111-1111-111111111117    Crawl Only         
    11111111-1111-1111-1111-111111111116    Cross-site Scripting Vulnerabilities       
    11111111-1111-1111-1111-111111111113    SQL Injection Vulnerabilities         
    11111111-1111-1111-1111-111111111118    quick_profile_2 0   {"wvs": {"profile": "continuous_quick"}}            
    11111111-1111-1111-1111-111111111114    quick_profile_1 0   {"wvs": {"profile": "continuous_full"}}         
    11111111-1111-1111-1111-111111111111    Full Scan   1   {"wvs": {"profile": "Default"}}         
    '''
    targets = getscan()
    if url in targets:
        return "repeat"
    else:
        target_id = addtask(url)
        data = {"target_id":target_id,"profile_id":"11111111-1111-1111-1111-111111111111","schedule": {"disable": False,"start_date":None,"time_sensitive": False}}
        try:
            response = requests.post(tarurl+"/api/v1/scans",data=json.dumps(data),headers=headers,timeout=30,verify=False)
            result = json.loads(response.content)
            return result['target_id']
        except Exception as e:
            print(str(e))
            return

def getstatus(scan_id):
    # Get the scanning status of scan_id
    try:
        response = requests.get(tarurl+"/api/v1/scans/"+str(scan_id),headers=headers,timeout=30,verify=False)
        result = json.loads(response.content)
        status = result['current_session']['status']
        #If it is completed, it means the end. A report can be generated
        if status == "completed":
            return getreports(scan_id)
        else:
            return result['current_session']['status']
    except Exception as e:
        print(str(e))
        return

def delete_scan(scan_id):
    # Delete the scan of scan_id
    try:
        response = requests.delete(tarurl+"/api/v1/scans/"+str(scan_id),headers=headers,timeout=30,verify=False)
        #If it is 204, it means the deletion is successful
        if response.status_code == "204":
            return True
        else:
            return False
    except Exception as e:
        print(str(e))
        return

def delete_target(target_id):
    # Delete the scan of scan_id
    try:
        response = requests.delete(tarurl+"/api/v1/targets/"+str(target_id),headers=headers,timeout=30,verify=False)
    except Exception as e:
        print(str(e))
        return    
    
def stop_scan(scan_id):
   # Stop scanning scan_id
    try:
        response = requests.post(tarurl+"/api/v1/scans/"+str(scan_id+"/abort"),headers=headers,timeout=30,verify=False)
        #If it is 204, it means the stop is successful
        if response.status_code == "204":
            return True
        else:
            return False
    except Exception as e:
        print(str(e))
        return    
    
def getreports(scan_id):
    # Get the scan report of scan_id
    '''
    11111111-1111-1111-1111-111111111111    Developer
    21111111-1111-1111-1111-111111111111    XML
    11111111-1111-1111-1111-111111111119    OWASP Top 10 2013 
    11111111-1111-1111-1111-111111111112    Quick
    '''
    data = {"template_id":"11111111-1111-1111-1111-111111111111","source":{"list_type":"scans","id_list":[scan_id]}}
    try:
        response = requests.post(tarurl+"/api/v1/reports",data=json.dumps(data),headers=headers,timeout=30,verify=False)
        result = response.headers
        report = result['Location'].replace('/api/v1/reports/','/reports/download/')
        return tarurl.rstrip('/')+report
    except Exception as e:
        print(str(e))
        return
    finally:
        delete_scan(scan_id)
        
# def generated_report(scan_id,target):
#     data = {"template_id": "21111111-1111-1111-1111-111111111111","source": {"list_type": "scans", "id_list":[scan_id]}}
#     try:
#         response = requests.post(tarurl + "/api/v1/reports", data=json.dumps(data), headers=headers, verify=False)
#         report_url = tarurl.strip('/') + response.headers['Location']
#         requests.get(str(report_url),headers=headers, verify=False)
#         while True:
#             report = get_report(response.headers['Location'])
#             if not report:
#                 time.sleep(5)
#             elif report:
#                 break
#         if(not os.path.exists("reports")):
#             os.mkdir("reports")
            
#         report = requests.get(tarurl + report,headers=headers, verify=False,timeout=120)
        
#         filename = str(target.strip('/').split('://')[1]).replace('.','_').replace('/','-')
#         file = "reports/" + filename + "%s.xml" % time.strftime("%Y-%m-%d-%H-%M", time.localtime(time.time()))
#         with open(file, "wb") as f:
#             f.write(report.content)
#         print("[INFO] %s report have %s.xml is generated successfully" % (target,filename))
#     except Exception as e:
#         raise e
#     finally:
#         delete_report(response.headers['Location'])
        
def get_report(reportid):
    res = requests.get(url=tarurl + reportid, timeout=10, verify=False, headers=headers)
    try:
        report_url = res.json()['download'][0]
        return report_url
    except Exception as e:
        return False
        
        
def config(url):
    target_id = addtask(url)
    # Get all scan status
    data = {
            "excluded_paths":["manager","phpmyadmin","testphp"],
            "user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "custom_headers":["Accept: */*","Referer:"+url,"Connection: Keep-alive"],
            "custom_cookies":[{"url":url,"cookie":"UM_distinctid=15da1bb9287f05-022f43184eb5d5-30667808-fa000-15da1bb9288ba9; PHPSESSID=dj9vq5fso96hpbgkdd7ok9gc83"}],
            "scan_speed":"moderate",#sequential/slow/moderate/fast more and more fast
            "technologies":["PHP"],#ASP,ASP.NET,PHP,Perl,Java/J2EE,ColdFusion/Jrun,Python,Rails,FrontPage,Node.js
            #acting
            "proxy": {
                "enabled":False,
                "address":"127.0.0.1",
                "protocol":"http",
                "port":8080,
                "username":"aaa",
                "password":"bbb"
            },
            # Login without verification code
            "login":{
                "kind": "automatic",
                "credentials": {
                    "enabled": False, 
                    "username": "test", 
                    "password": "test"
                }
            },
            #401 authentication
            "authentication":{
                "enabled":False,
                "username":"test",
                "password":"test"
            }
        }
    try:
        res = requests.patch(tarurl+"/api/v1/targets/"+str(target_id)+"/configuration",data=json.dumps(data),headers=headers,timeout=30*4,verify=False)
        
        data = {"target_id":target_id,"profile_id":"11111111-1111-1111-1111-111111111111","schedule": {"disable": False,"start_date":None,"time_sensitive": False}}
        try:
            response = requests.post(tarurl+"/api/v1/scans",data=json.dumps(data),headers=headers,timeout=30,verify=False)
            result = json.loads(response.content)
            return result['target_id']
        except Exception as e:
            print(str(e))
            return
    except Exception as e:
        raise e
        
def getscan():
    # Get all scan status
    targets = []
    try:
        response = requests.get(tarurl+"/api/v1/scans",headers=headers,timeout=30,verify=False)
        results = json.loads(response.content)
        for result in results['scans']:
            targets.append(result['target']['address'])
            print (result['scan_id'],result['target']['address'],getstatus(result['scan_id']))#,result['target_id']
        return list(set(targets))
    except Exception as e:
        raise e

# https://localhost:13443/api/v1/scans/bfbb3128-7abe-40e5-96f9-cf228f2e213d/results/ -> get result id 
def get_result_id(scan_id: str): 
    if len(scan_id) == 0: return
    res = get_request('scans/' + scan_id + '/results')
    return json.loads(res.content)['results'][0]['result_id']

# https://localhost:13443/api/v1/scans/bfbb3128-7abe-40e5-96f9-cf228f2e213d/results/e039d822-6dd5-479b-8a1d-ea26a2cb5643/vulnerabilities -> get list loi~
def get_list_vuln(scan_id: str, result_id: str):
    # condition if result if not exist
    res = get_request('scans/' + scan_id + '/results/' + result_id + '/vulnerabilities')
    arr = json.loads(res.content)['vulnerabilities']
    results = format_vuln_output(arr)
    print(results)
    return results


def format_vuln_output(array: list):
    if len(array) == 0: return
    list_results = []
    for e in array: 
        # element = {
        #     'severity': e['severity'],
        #     'vuln_name': e['vt_name'],
        #     'param': e['affects_detail'],
        #     'url_location': e['affects_url']
        # }
        output = f"[Severity] {e['severity']} || [Vuln Name] {e['vt_name']}"
        list_results.append(output)
    return list_results


def getstatuscode(scan_id):
    try:
        response = requests.get(tarurl+"/api/v1/scans/"+str(scan_id),headers=headers,timeout=30,verify=False)
        result = json.loads(response.content)
        status = result['current_session']['status']
        #If it is completed, it means the end. A report can be generated
        if status == "completed":
            return 1
        else:
            return 0
    except Exception as e:
        print(str(e))
        return
    

def print_scan_report(scan_id):
    headers = {
        "X-Auth": apikey,
        "Content-Type": "application/json"
    }
    url = f"{tarurl}/scans/{scan_id}/report"
    response = requests.get(url, headers=headers)
    report = response.json()
    print(report)


def config_list(arr: list):
    ids = []
    for domain in arr:
        id = config(domain)
        ids.append(id)
    return ids


def process(scan_ids):
    completed_scans = set()

    while True:
        for scan_id in scan_ids:
            if scan_id in completed_scans:
                continue  # Skip if the scan has already been completed

            scan_status = getstatuscode(scan_id)
            if scan_status == 1:
                completed_scans.add(scan_id)
                print(f"Scan ID: {scan_id}")
                print_scan_report(scan_id)
                print("=" * 50)

        if len(completed_scans) == len(scan_ids):
            break  # Break the loop if all scans are completed

        time.sleep(60)  # Wait for 1 minute before checking again

def get_request(url: str):
    if len(url) == 0: return
    baseUrl = tarurl + '/api/v1/'
    return requests.get(baseUrl + url,headers=headers,timeout=30,verify=False)

if __name__ == '__main__':
    print (config('http://testhtml5.vulnweb.com/'))
