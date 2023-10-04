import os
import subprocess


def _run(cmd):
    # Mock this for testing
    return subprocess.run(cmd)


def extract_output(out):
    return out.replace('"', "")


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


def job_metadata(jobid=None):
    if jobid is None:
        jobid = os.environ.get("SLURM_JOB_ID")

    command = ["squeue", "-h", f"--job={jobid}", '--format="%k"']

    output = subprocess.check_output(command, text=True)
    output = extract_output(output)

    meta = dict()
    for line in output.splitlines():
        meta.update(parse_meta(line))

    return meta


def set_comment(comment: str):
    jobid = os.environ.get("SLURM_JOB_ID")

    command = [
        "scontrol",
        "update",
        "job",
        f"{jobid}",
        f"comment={comment}",
    ]

    _run(command)


def update_comment(*metdata):
    original = job_metadata()

    for kv in metdata:
        k, v = kv.split("=")
        original[k] = v

    newcomment = []
    for k, v in original.items():
        newcomment.append(f"{k}={v}")
    newcomment = "|".join(newcomment)

    set_comment(newcomment)
    print(newcomment)