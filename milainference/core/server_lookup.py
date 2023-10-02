import subprocess
import random


def get_slurm_job_by_name(name):
    """Retrieve a list of jobs that match a given job name"""
    command = ["squeue", "-h", f"--name={name}", "--format=\"%A %j %T %P %U %k %N\""]

    output = subprocess.check_output(command, text=True)
    jobs = []

    def parse_meta(comment):
        data = dict()
        if comment != "(null)":
            items = comment.split('|')
            for kv in items:
                try:
                    k, v = kv.split('=', maxsplit=1)
                    data[k] = v
                except: 
                    pass

        return data

    for line in output.splitlines():
        job_id, job_name, status, partition, user, comment, nodes = line.split(' ')
        
        jobs.append({
            "job_id":job_id, 
            "job_name":job_name, 
            "status":status,
            "partition":partition, 
            "user":user,
            "comment": parse_meta(comment),
            "nodes": nodes
        })

    return jobs



def find_suitable_inference_server(jobs, model):
    """Select suitable jobs from a list, looking for a specific model"""
    selected = []
    
    def is_shared(job):
        return job["comment"].get("shared", 'y') == 'y'
    
    def is_running(job):
        return job['status'] == "RUNNING"
    
    def has_model(job, model):
        if model is None:
            return True
        return job['comment']['model'] == model
    
    def select(job):
        selected.append({
            "model": job['comment']["model"],
            "host": job["comment"]["host"],
            "port": job["comment"]["port"],
        })
            
    for job in jobs:
        if is_shared(job) and is_running(job) and has_model(job, model):
            select(job)
                
    return selected


def get_inference_server(model=None):
    """Retrieve an inference server from slurm jobs"""
    jobs = get_slurm_job_by_name('inference_server_SHARED.sh')

    servers = find_suitable_inference_server(jobs, model)

    try:
        return random.choice(servers)
    except IndexError:
        return None


def get_endpoint(model):
    server = get_inference_server(model)
    
    return f"http://{server['host']}:{server['port']}/v1"



