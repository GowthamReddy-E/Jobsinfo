import os
import jenkins
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
    job_info = []
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

        job_info.append({
            'job_name': job['name'],
            'current_build_number': current_build_number,
            'last_successful_build_number': last_successful_build_number,
            'last_failed_build_number': last_failed_build_number,
            'build_triggering_time': build_triggering_time,
            'build_duration': build_duration_str,
            'current_build_status': current_build_status,  # Include current build status
        })

    return job_info

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
server_url = 'http://localhost:8080/'
username = 'gowthame'
api_token = '11f513f52837b01d30f3d0ef3925806e97'

# Connect to Jenkins server
server = connect_to_jenkins(server_url, username, api_token)

# Get all jobs from Jenkins
jobs = get_jenkins_jobs(server)

# Retrieve job information
job_info = get_jenkins_job_info(server, jobs)

# Store console logs in a given path
logs_directory = '/Users/gowe/Desktop/MyWork/githubWorkspace/Jobsinfo/logs/'  # Update this with the desired path

for job in job_info:
    # Get console log for the current build of the job
    console_log = get_console_log(server, job['job_name'], job['current_build_number'])
    
    # Generate log filename with current build status
    log_filename = f"{job['job_name']}_{job['current_build_number']}_{job['current_build_status'].lower()}.log"
    log_filepath = os.path.join(logs_directory, log_filename)
    
    # Write console log to file
    write_log_to_file(console_log, log_filepath)
    print(f"Console log for {job['job_name']} saved to {log_filepath}")



# Print job information
for job in job_info:
    print("\n")
    print(f"Job Name: {job['job_name']}")
    print(f"Current Build Number: {job['current_build_number']}")
    print(f"Current Build Status: {job['current_build_status']}")
    print(f"Last Successful Build Number: {job['last_successful_build_number']}")
    print(f"Last Failed Build Number: {job['last_failed_build_number']}")
    print(f"Build Triggering Time: {job['build_triggering_time']}")
    print(f"Build Duration: {job['build_duration']}")
    print("\n")


import os

def get_files_info(directory_path):
    """
    Retrieve file information from a directory.
    """
    files_list = []

    # Check if the directory exists
    if os.path.exists(directory_path):
        # Iterate through files in the directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            # Check if it's a file
            if os.path.isfile(file_path):
                # Store filename in the list
                files_list.append(filename)
    else:
        print(f"Directory '{directory_path}' does not exist.")

    return files_list

def get_files_size(directory_path, files_list):
    """
    Retrieve size of files and store in a dictionary with job name as key.
    """
    files_size_dict = {}

    # Iterate through the list of filenames
    for filename in files_list:
        file_path = os.path.join(directory_path, filename)
        # Get the size of the file
        file_size = os.path.getsize(file_path)
        # Extract job name from filename (assuming filename is in the format 'jobname_buildnumber_console.log')
        job_name = filename.split('_')[0]  # Assuming job name is before the first underscore
        # Store job name and size in the dictionary
        files_size_dict[job_name] = file_size

    return files_size_dict

# Example usage
directory_path = '/Users/gowe/Desktop/MyWork/githubWorkspace/Jobsinfo/logs/'
files_list = get_files_info(directory_path)
files_size_dict = get_files_size(directory_path, files_list)

print(files_list)
print(files_size_dict)