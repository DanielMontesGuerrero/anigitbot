import github3
from github3.pulls import PullRequest
from github3.structs import GitHubIterator

class GithubHandler:
    def __init__(self, token: str):
        self.client = github3.login(token=token)
        if self.client is None:
            raise Exception('Can not connect github client')

    def get_pull_requests(self, user: str, repository_name: str, state: str = 'open') -> GitHubIterator:
        repository = self.client.repository(user, repository_name)
        pull_requests = repository.pull_requests(state=state)
        return pull_requests
