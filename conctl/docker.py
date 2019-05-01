from typing import Dict, List

from conctl.base import ContainerRuntimeCtlBase, CompletedProcess


class DockerCtl(ContainerRuntimeCtlBase):
    """
    Control Containerd via `docker`.
    """
    def __init__(self) -> None:
        """
        :return: None
        """
        super().__init__()
        self.runtime = 'docker'

    def _exec(self, *args: List[str]) -> CompletedProcess:
        """
        Run `docker`.

        :param args: List args
        :return: CompletedProcess
        """
        return super()._exec(*['docker'] + list(args))

    def run(self,
            name: str,
            image: str,
            mounts: Dict[str, str],
            environment: Dict[str, str],
            command: str = None,
            *args: List[str]) -> CompletedProcess:
        """
        Run a container.

        :param name: String
        :param image: String
        :param mounts: Dictionary String host path String container path
        :param environment: Dictionary String key String value
        :param command: String
        :param args: List String
        :return: CompletedProcess
        """
        to_run: list = [
            'run',
            '--name', name
        ]

        for host, container in mounts.items():
            to_run.append('--volume')
            to_run.append('{}:{}'.format(host, container))

        for key, value in environment.items():
            to_run.append('--env')
            to_run.append('{}={}'.format(key, value))

        to_run.append(image)

        if command:
            to_run.append(command)
            to_run += args

        return self._exec(*to_run)

    def delete(self, *container_ids) -> CompletedProcess:
        """
        Delete a container.

        :param container_ids: String
        :return: CompletedProcess
        """
        return self._exec(
            'rm', '-f', *container_ids
        )
