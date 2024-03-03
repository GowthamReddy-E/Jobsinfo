import os
import jenkins
import json
from datetime import datetime

def connect_to_jenkins(server_url, username, api_token):
    """
    Connect to Jenkins server.
    """
    return jenkins.Jenkins(server_url, username=username, password=api_token)

def get_build_info(server, job_name, build_number):
    """
    Retrieve build information for a specific job and build number.
    """
    return server.get_build_info(job_name, build_number)

def get_build_duration(build_info):
    """
    Calculate build duration in a human-readable format.
    """
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
    """
    Retrieve information for all jobs in Jenkins.
    """
    job_info = {}
    current_build_numbers = {}  # Dictionary to store current build number for each job

    for job in jobs:
        job_details = server.get_job_info(job['name'])

        current_build_number = None
        last_successful_build_number = None
        last_failed_build_number = None
        build_triggering_time = None
        build_duration_str = None
        current_build_status = None  # Initialize current build status

        if job_details['lastBuild'] is not None:
            current_build_number = job_details['lastBuild']['number']
            last_build_info = get_build_info(server, job['name'], current_build_number)
            last_successful_build_number = job_details['lastSuccessfulBuild']['number'] if job_details['lastSuccessfulBuild'] else None
            last_failed_build_number = job_details['lastFailedBuild']['number'] if job_details['lastFailedBuild'] else None

            build_triggering_time = datetime.fromtimestamp(last_build_info['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            build_duration_str = get_build_duration(last_build_info)

            # Check if build status is "ABORTED" and update accordingly
            current_build_status = last_build_info['result']
            if current_build_status is None:
                current_build_status = 'ABORTED'

        job_name = job['name']
        cur_build_name = f"{job_name}"
        
        # Store current build number as string with 'cur_' prefix
        job_info[job_name] = {
            'current_build_name': cur_build_name,
            'current_build_number': str(current_build_number),
            'last_successful_build_number': last_successful_build_number,
            'last_failed_build_number': last_failed_build_number,
            'build_triggering_time': build_triggering_time,
            'build_duration': build_duration_str,
            'current_build_status': current_build_status,  # Include current build status
        }
        
        # Store current build number separately in a dictionary
        current_build_numbers[cur_build_name] = current_build_number

    return job_info, current_build_numbers

def get_jenkins_jobs(server):
    """
    Retrieve all jobs from Jenkins.
    """
    return server.get_all_jobs()

def get_console_log(server, job_name, build_number):
    """
    Retrieve console log for a specific build of a job.
    """
    return server.get_build_console_output(job_name, build_number)

def write_log_to_file(log_content, log_filepath):
    """
    Write console log content to a file.
    """
    with open(log_filepath, 'w') as log_file:
        log_file.write(log_content)

# Example usage
server_url = 'http://localhost:9090/'
username = 'admin'
api_token = '11c433081e76b2b952d517d3aa146687b7'

# Connect to Jenkins server
server = connect_to_jenkins(server_url, username, api_token)

# Get all jobs from Jenkins
jobs = get_jenkins_jobs(server)

# Retrieve job information
job_info, current_build_numbers = get_jenkins_job_info(server, jobs)

# Store console logs in a given path
logs_directory = 'F:/gowthamCodingProjects/GitHub/myRepositaryProjects/Jobsinfo/logs'  # Update this with the desired path

job_statuses = {}

# Extract job name and status and store them in the dictionary
for job_name, info in job_info.items():
    job_statuses[job_name] = info['current_build_status'].lower()

# Print the dictionary containing job names with their statuses
print(job_statuses)

# Save job information to a JSON file
json_filepath = 'F:/gowthamCodingProjects/GitHub/myRepositaryProjects/Jobsinfo/job_info.json'  # Update this with the desired path
with open(json_filepath, 'w') as json_file:
    json.dump(job_info, json_file, indent=4)


# Load the JSON data from the file
# json_filepath = 'F:/gowthamCodingProjects/GitHub/myRepositaryProjects/Jobsinfo/job_info.json'

with open(json_filepath, 'r') as json_file:
    data = json.load(json_file)

# Initialize an empty dictionary to store the extracted data
Current_data = {}

# Extract the required information for each job
for job_name, job_info in data.items():
    Current_data[job_name] = int(job_info['current_build_number'])

# logs_directory = "F:/gowthamCodingProjects/GitHub/myRepositaryProjects/Jobsinfo/logs"

def extract_job_name(filename):
    parts = filename.split('_')
    if len(parts) > 2:
        return '_'.join(parts[:-2])
    else:
        return parts[0]

# Function to extract build number from log file name
def extract_build_number(filename):
    return int(filename.split('_')[-2])

# Function to get list of existing log files and their build numbers
def get_existing_files(logs_directory):
    existing_files = {}
    log_files = os.listdir(logs_directory)
    for filename in log_files:
        job_name = extract_job_name(filename)
        build_number = extract_build_number(filename)
        existing_files[job_name] = build_number
    return existing_files

# Path to your logs directory

# Get existing log files and their build numbers
existing_data = get_existing_files(logs_directory)

# Print the dictionary containing filename and build number



# Function to extract job name from log file name
def extract_job_name(filename):
    parts = filename.split('_')
    if len(parts) > 2:
        return '_'.join(parts[:-2])
    else:
        return parts[0]

# Function to get list of existing log files
def get_existing_files(logs_directory):
    files_list = []  # List to store filenames
    log_files = os.listdir(logs_directory)
    for filename in log_files:
        files_list.append(filename)
    return files_list

# Path to your logs directory

# Get list of existing log files
existing_names = get_existing_files(logs_directory)

# Print the list containing filenames




# Load the JSON data from the file
json_filepath = 'F:/gowthamCodingProjects/GitHub/myRepositaryProjects/Jobsinfo/job_info.json'

with open(json_filepath, 'r') as json_file:
    data = json.load(json_file)

# Initialize an empty list to store the extracted job names
Current_names = []

# Extract job names from the JSON data
for job_name in data.keys():
    Current_names.append(job_name)

# Print the list of job names
print(Current_names)
print(Current_data)
print(existing_data)
print(existing_names)



# ===================================================

        
job_logs = {}

# Retrieve console log for each job and store it in the dictionary
for job in jobs:
    job_name = job['name']
    last_build_info = server.get_job_info(job_name)['lastBuild']
    if last_build_info is not None:
        build_number = last_build_info['number']
        console_log = get_console_log(server, job_name, build_number)
        job_logs[job_name] = console_log

# Save job names to a list
job_names = list(job_logs.keys())

print(job_names)

# ===========================================================

def process_existing_files(Current_names, existing_names, Current_data, existing_data, logs_directory):
    if len(existing_names) != 0:
        for i in range(len(Current_names)):
            for j in range(len(existing_names)):
                if Current_names[i].lower() in existing_names[j].lower() and 'failure' not in existing_names[j].lower():
                    if Current_data[Current_names[i]] - existing_data[Current_names[j]] >= 1:
                        # Delete the file from the logs directory
                        os.remove(os.path.join(logs_directory, existing_names[j]))
                        print("Log file Deleted for job:", Current_names[i])
                    else:
                        # Create a log file with the current job name
                        selected_job_name = Current_names[i]
                        log_content = job_logs[selected_job_name]
                        log_filename = f"{Current_names[i]}_{Current_data[Current_names[i]]}_{job_statuses[Current_names[i]]}.log"
                        log_filepath = os.path.join(logs_directory, log_filename)
                        write_log_to_file(log_content, log_filepath)               
                        print(f"Log file created for job: {selected_job_name}")    
                elif Current_names[i].lower() in existing_names[j].lower() and 'failure'  in existing_names[j].lower():
                    print("create a file")
                    selected_job_name = Current_names[i]
                    log_content = job_logs[selected_job_name]
                    log_filename = f"{Current_names[i]}_{Current_data[Current_names[i]]}_{job_statuses[Current_names[i]]}.log"
                    log_filepath = os.path.join(logs_directory, log_filename)
                    write_log_to_file(log_content, log_filepath)               
                    print(f"Log file created for job: {selected_job_name}")
                       
    else:
         for i in range(len(Current_names)):
            selected_job_name = Current_names[i]
            log_content = job_logs[selected_job_name]
            log_filename = f"{Current_names[i]}_{Current_data[Current_names[i]]}_{job_statuses[Current_names[i]]}.log"
            log_filepath = os.path.join(logs_directory, log_filename)
            write_log_to_file(log_content, log_filepath)
            print("Log file created for job:", Current_names[i])     

process_existing_files(Current_names, existing_names, Current_data, existing_data, logs_directory)



