"""This pre-commit hook allows to run pytest tests in docker."""
import sys

from docker_pytest.docker_utils import (is_docker_compose_available,
                                        is_docker_daemon_running,
                                        is_valid_docker_compose_config,
                                        run_tests_docker)

# TODO check pytest call
# TODO handle docker startup errors


def main() -> int:
    filenames = sys.argv[1:]

    if len(filenames) != 1:
        print('Exactly one docker-compose file must be specified.')
        return 1

    config_file = filenames[0]

    if not is_docker_compose_available():
        print('docker-compose is not available.')
        return 1

    if not is_docker_daemon_running():
        print('Docker daemon is not running.')
        return 1

    is_valid, error_msg = is_valid_docker_compose_config(config_file)
    if not is_valid:
        print(error_msg)
        return 1

    retval, msg = run_tests_docker(config_file)
    print(msg)
    if retval == 0:
        return 0
    return 1


if __name__ == '__main__':
    main()
