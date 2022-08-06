import subprocess


def is_docker_compose_available() -> bool:
    cp = subprocess.run(['docker-compose', '--version'], capture_output=True)
    if cp.returncode == 0:
        return True
    return False


def is_docker_daemon_running() -> bool:
    cp = subprocess.run(['docker', 'stats', '--no-stream'],
                        capture_output=True)
    if cp.returncode == 0:
        return True
    return False


def is_valid_docker_compose_config(filename: str) -> tuple[bool, str | None]:
    cp = subprocess.run(['docker-compose', '-f', filename, 'config'],
                        capture_output=True, encoding='utf-8')
    if cp.returncode == 0:
        return True, None
    return False, cp.stderr


def get_pytest_output(s: str) -> str:
    start = s.find('test session start') - 2
    while s[start] == '=':
        start -= 1
    start += 1
    end = s.rfind('=') + 1
    return s[start:end]


def run_tests_docker(config: str) -> tuple[int, str]:
    cp = subprocess.run(
        [
            'docker-compose',
            '-f',
            config,
            'up',
            '--abort-on-container-exit',
            '--no-log-prefix',
        ],
        capture_output=True,
        encoding='utf-8'
    )
    msg = ''
    try:
        msg = get_pytest_output(cp.stdout)
    except IndexError:
        pass
    finally:
        subprocess.run(['docker-compose', '-f', config, 'down'],
                       capture_output=True)
    return cp.returncode, msg

# TODO Handle tests fail and docker crash
# TODO Docker problems message
# TODO Pretty colorful output
