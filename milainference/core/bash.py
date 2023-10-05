import subprocess


def run(cmd):
    # Mock this for testing
    return subprocess.run(cmd)


def popen(cmd, callback=None):
    def println(line):
        print(line, end="")

    if callback is None:
        callback=println
    
    with subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        shell=False,
    ) as process:
        def readoutput():
            process.stdout.flush()
            line = process.stdout.readline()

            if callback:
                callback(line)

        try:
            while process.poll() is None:
                readoutput()

            readoutput()
            return 0

        except KeyboardInterrupt:
            print("Stopping due to user interrupt")
            process.kill()
            return -1
