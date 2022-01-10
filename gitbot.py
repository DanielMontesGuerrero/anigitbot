from dataclasses import dataclass
import re
from typing import Callable

import discord
import github3

@dataclass
class Command:
    separator: str
    name: str
    handle: Callable

    def match(self, message) -> bool:
        return message.content.startswith(self.separator + self.name)

class Gitbot(discord.Client):
    def __init__(self, command_symbol='!', *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'github_token' not in kwargs:
            raise   Exception('Missing github token')
        self.github = github3.login(token=kwargs['github_token'])
        self.command_symbol = command_symbol
        self.commands = [
            Command(self.command_symbol, 'pr', self.on_pr_command),
        ]

    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        for command in self.commands:
            if command.match(message):
                return await command.handle(message)

    async def on_pr_command(self, message):
        args = self.parse_args(message)
        if 'user' not in args or 'name' not in args:
            return await self.send_error_message(message, 'Missing --user and --name')
        user = args['user']
        repository_name = args['name']
        state = 'open'
        if 'state' in args:
            state = args['state']
        repository = self.github.repository(user, repository_name)
        pull_requests = repository.pull_requests(state=state)
        res = ''
        for i, pr in enumerate(pull_requests):
            res += f"{i}. Title: {pr.title}, state: {pr.state}\n"
        res = (res[:1995] + '...') if len(res) > 2000 else res
            # print(f"""
            # Titulo: {pr.title}
            # state: {pr.state}
            # User id: {pr.user.id}
            #   """)
        await message.channel.send(res)

    def parse_args(self, message):
        words_in_message = message.content.split(' ')
        args = {}
        for index, word in enumerate(words_in_message):
            if re.search(r'^--\w+$', word) and (index + 1) < len(words_in_message):
                key = word[2:]
                value = words_in_message[index + 1]
                if re.search(r'^\d+$', value):
                    value = int(value)
                args[key] = value
        return args

    async def send_error_message(self, message, description):
        return await message.send(description)
