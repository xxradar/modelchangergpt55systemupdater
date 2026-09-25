import subprocess

DOCKER_HOST = "unix:///run/docker.sock"

def run_cmd(args):
    cmd = ["docker", "-H", DOCKER_HOST] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
    return result

if __name__ == "__main__":
    run_cmd(["ps"])
    run_cmd(["run", "-d", "--name", "www", "nginx"])
    run_cmd(["ps"])
