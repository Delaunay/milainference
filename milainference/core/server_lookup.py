import subprocess
import random
import datetime

#
#
#


# %e Time at which the job ended or is expected to end
# %L Time left for the job to execute in days-hours:minutes:seconds.


def _fetch_job_info(name):
    # Mock this for testing
    command = ["squeue", "-h", f"--name={name}", '--format="%A %j %T %P %U %k %N %L"']
    return subprocess.check_output(command, text=True)


def parse_meta(comment):
    data = dict()
    if comment != "(null)":
        items = comment.split("|")
        for kv in items:
            try:
                k, v = kv.split("=", maxsplit=1)
                data[k] = v
            except:
                pass

    return data


def get_slurm_job_by_name(name):
    """Retrieve a list of jobs that match a given job name"""

    output = _fetch_job_info(name)
    jobs = []

    for line in output.splitlines():
        (
            job_id,
            job_name,
            status,
            partition,
            user,
            comment,
            nodes,
            timeleft,
        ) = line.split(" ")

        hours, minutes, seconds = timeleft.split(":")
        timeleft = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        jobs.append(
            {
                "job_id": job_id,
                "job_name": job_name,
                "status": status,
                "partition": partition,
                "user": user,
                "comment": parse_meta(comment),
                "nodes": nodes,
                "timeleft": timeleft,
            }
        )

    return jobs


def find_suitable_inference_server(jobs, model):
    """Select suitable jobs from a list, looking for a specific model"""
    selected = []

    def is_shared(job):
        return job["comment"].get("shared", "y") == "y"

    def is_running(job):
        timeleft = job["timeleft"]

        return job["status"] == "RUNNING" and timeleft.total_seconds() > 20

    def is_ready(job):
        return job["comment"].get("ready", "0") == "1"

    def has_model(job, model):
        if model is None:
            return True

        # FIXME:
        #   /network/weights/llama.var/llama2/Llama-2-7b-hf != meta-llama/Llama-2-7b-hf
        #
        return job["comment"]["model"] == model

    def select(job):
        selected.append(
            {
                "model": job["comment"]["model"],
                "host": job["comment"]["host"],
                "port": job["comment"]["port"],
            }
        )

    for job in jobs:
        if (
            True
            and is_shared(job)
            and is_running(job)
            and has_model(job, model)
            and is_ready(job)
        ):
            select(job)

    return selected


def get_inference_servers(model=None):
    """Retrieve an inference server from slurm jobs"""

    jobs = get_slurm_job_by_name("inference_server_SHARED.sh")
    servers = find_suitable_inference_server(jobs, model)
    return servers


def select_inferences_server(model):
    servers = get_inference_servers(model)

    try:
        return random.choice(servers)
    except IndexError:
        return None


def get_endpoint(model):
    server = select_inferences_server(model)

    return f"http://{server['host']}:{server['port']}/v1"
