import os
import jenkins
import json
from datetime import datetime

def connect_to_jenkins(server_url, username, api_token):
    return jenkins.Jenkins(server_url, username=username, password=api_token)

def get_build_info(server, job_name, build_number):
    return server.get_build_info(job_name, build_number)

def get_build_duration(build_info):
    build_start_time = datetime.fromtimestamp(build_info['timestamp'] / 1000)
    build_end_time = datetime.fromtimestamp((build_info['timestamp'] + build_info['duration']) / 1000)

    build_duration = build_end_time - build_start_time

    total_seconds = build_duration.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds % 1) * 1000)

    return f"{hours} hr {minutes} min {seconds} sec {milliseconds} ms"

def get_jenkins_job_info(server, jobs):
    job_info = {}
    current_build_numbers = {}

    for job in jobs:
        job_details = server.get_job_info(job['name'])

        current_build_number = None
        last_successful_build_number = None
        last_failed_build_number = None
        build_triggering_time = None
        build_duration_str = None
        current_build_status = None

        if job_details['lastBuild'] is not None:
            current_build_number = job_details['lastBuild']['number']
            last_build_info = get_build_info(server, job['name'], current_build_number)
            last_successful_build_number = job_details['lastSuccessfulBuild']['number'] if job_details['lastSuccessfulBuild'] else None
            last_failed_build_number = job_details['lastFailedBuild']['number'] if job_details['lastFailedBuild'] else None

            build_triggering_time = datetime.fromtimestamp(last_build_info['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            build_duration_str = get_build_duration(last_build_info)

            current_build_status = last_build_info['result']
            if current_build_status is None:
                current_build_status = 'ABORTED'

        job_name = job['name']
        cur_build_name = f"{job_name}"
        
        job_info[job_name] = {
            'current_build_name': cur_build_name,
            'current_build_number': str(current_build_number),
            'last_successful_build_number': last_successful_build_number,
            'last_failed_build_number': last_failed_build_number,
            'build_triggering_time': build_triggering_time,
            'build_duration': build_duration_str,
            'current_build_status': current_build_status,
        }
        
        current_build_numbers[cur_build_name] = current_build_number

    return job_info, current_build_numbers

def get_jenkins_jobs(server):
    return server.get_all_jobs()

def get_console_log(server, job_name, build_number):
    return server.get_build_console_output(job_name, build_number)

def write_log_to_file(log_content, log_filepath):
    with open(log_filepath, 'w') as log_file:
        log_file.write(log_content)

server_url = 'http://192.168.1.3:9090/'
username = 'admin'
api_token = '11c433081e76b2b952d517d3aa146687b7'

server = connect_to_jenkins(server_url, username, api_token)
jobs = get_jenkins_jobs(server)
job_info, current_build_numbers = get_jenkins_job_info(server, jobs)
logs_directory = 'F:/gowthamCodingProjects/GitHub/myRepositaryProjects/Jobsinfo/logs'
# logs_directory = '/logs'

job_statuses = {}
for job_name, info in job_info.items():
    job_statuses[job_name] = info['current_build_status'].lower()

print(job_statuses)

json_filepath = 'F:/gowthamCodingProjects/GitHub/myRepositaryProjects/Jobsinfo/data.json'
# json_filepath = '/data.json'


with open(json_filepath, 'w') as json_file:
    json.dump(job_info, json_file, indent=4)

with open(json_filepath, 'r') as json_file:
    data = json.load(json_file)

Current_data = {}
for job_name, job_info in data.items():
    Current_data[job_name] = int(job_info['current_build_number'])

def extract_job_name(filename):
    parts = filename.split('_')
    if len(parts) > 2:
        return '_'.join(parts[:-2])
    else:
        return parts[0]

def extract_build_number(filename):
    return int(filename.split('_')[-2])

def get_existing_files(logs_directory):
    existing_files = {}
    log_files = os.listdir(logs_directory)
    for filename in log_files:
        job_name = extract_job_name(filename)
        build_number = extract_build_number(filename)
        existing_files[job_name] = build_number
    return existing_files

existing_data = get_existing_files(logs_directory)

def extract_job_name(filename):
    parts = filename.split('_')
    if len(parts) > 2:
        return '_'.join(parts[:-2])
    else:
        return parts[0]

def get_existing_files(logs_directory):
    files_list = []
    log_files = os.listdir(logs_directory)
    for filename in log_files:
        files_list.append(filename)
    return files_list

existing_names = get_existing_files(logs_directory)

# json_filepath = 'F:/gowthamCodingProjects/GitHub/myRepositaryProjects/Jobsinfo/data.json'
with open(json_filepath, 'r') as json_file:
    data = json.load(json_file)

Current_names = []
for job_name in data.keys():
    Current_names.append(job_name)

job_logs = {}
for job in jobs:
    job_name = job['name']
    last_build_info = server.get_job_info(job_name)['lastBuild']
    if last_build_info is not None:
        build_number = last_build_info['number']
        console_log = get_console_log(server, job_name, build_number)
        job_logs[job_name] = console_log

job_names = list(job_logs.keys())

def process_existing_files(Current_names, existing_names, Current_data, existing_data, logs_directory):
    if len(existing_names) != 0:
        for i in range(len(Current_names)):
            for j in range(len(existing_names)):
                if Current_names[i].lower() in existing_names[j].lower() and 'failure' not in existing_names[j].lower():
                    if Current_data[Current_names[i]] - existing_data[Current_names[j]] >= 1:
                        os.remove(os.path.join(logs_directory, existing_names[j]))
                        print("Log file Deleted for job:", Current_names[i])
                        selected_job_name = Current_names[i]
                        log_content = job_logs[selected_job_name]
                        log_filename = f"{Current_names[i]}_{Current_data[Current_names[i]]}_{job_statuses[Current_names[i]]}.log"
                        log_filepath = os.path.join(logs_directory, log_filename)
                        try:
                            write_log_to_file(log_content, log_filepath)
                            print("Log file created for job:", Current_names[i])
                        except UnicodeEncodeError as e:
                            print(f"UnicodeEncodeError: {e}")
                            print("The Log file Can not be created it's not readable format job:", Current_names[i])
                    else:
                        selected_job_name = Current_names[i]
                        log_content = job_logs[selected_job_name]
                        log_filename = f"{Current_names[i]}_{Current_data[Current_names[i]]}_{job_statuses[Current_names[i]]}.log"
                        log_filepath = os.path.join(logs_directory, log_filename)
                        try:
                            write_log_to_file(log_content, log_filepath)
                            print("Log file created for job:", Current_names[i])
                        except UnicodeEncodeError as e:
                            print(f"UnicodeEncodeError: {e}")
                            print("The Log file Can not be created it's not readable format job:", Current_names[i])    
                elif Current_names[i].lower() in existing_names[j].lower() and 'failure'  in existing_names[j].lower():
                    selected_job_name = Current_names[i]
                    log_content = job_logs[selected_job_name]
                    log_filename = f"{Current_names[i]}_{Current_data[Current_names[i]]}_{job_statuses[Current_names[i]]}.log"
                    log_filepath = os.path.join(logs_directory, log_filename)
                    try:
                        write_log_to_file(log_content, log_filepath)
                        print("Log file created for job:", Current_names[i])
                    except UnicodeEncodeError as e:
                        print(f"UnicodeEncodeError: {e}")
                        print("The Log file Can not be created it's not readable format job:", Current_names[i])
                       
    else:
         for i in range(len(Current_names)):
            selected_job_name = Current_names[i]
            log_content = job_logs[selected_job_name]
            log_filename = f"{Current_names[i]}_{Current_data[Current_names[i]]}_{job_statuses[Current_names[i]]}.log"
            log_filepath = os.path.join(logs_directory, log_filename)
            try:
                write_log_to_file(log_content, log_filepath)
                print("Log file created for job:", Current_names[i])
            except UnicodeEncodeError as e:
                print(f"UnicodeEncodeError: {e}")
                print("The Log file Can not be created it's not readable format job:", Current_names[i])     

process_existing_files(Current_names, existing_names, Current_data, existing_data, logs_directory)

print(Current_names)
print(existing_names)
print(Current_data)
print(job_statuses)

