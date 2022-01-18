import sys
import os

from flask import Flask, request
from src.anigitrest import Anigitrest
from src.db import db
from src.db.models import NotifyList


app = Flask('anigitbot_server')

@app.route('/')
async def serve():
    return 'Sup bro'

@app.route('/pr')
async def pull_request():
    try:
        data = request.args
        discord_token, github_token = config()
        channel_id = int(data.get('channel_id', ''))
        user = data.get('user', '')
        repository_name = data.get('repo', '')
        pr_number = int(data.get('pr', ''))
        anigitrest = Anigitrest(discord_token=discord_token, github_token=github_token)
        await anigitrest.notify_pull_request(
            channel_id,
            user,
            repository_name,
            pr_number,
        )
        return 'Success'
    except KeyError:
        return 'Missing argumetns'

@app.route('/issue')
async def issue():
    try:
        data = request.args
        discord_token, github_token = config()
        channel_id = int(data.get('channel_id', ''))
        user = data.get('user', '')
        repository_name = data.get('repo', '')
        pr_number = int(data.get('issue', ''))
        anigitrest = Anigitrest(discord_token=discord_token, github_token=github_token)
        await anigitrest.notify_issue(
            channel_id,
            user,
            repository_name,
            pr_number,
        )
        return 'Success'
    except KeyError:
        return 'Missing argumetns'

def config():
    if len(sys.argv) > 1:
        discord_token = sys.argv[1]
    else:
        discord_token = os.getenv('DISCORD_TOKEN')
    if len(sys.argv) > 2:
        github_token = sys.argv[2]
    else:
        github_token = os.getenv('GITHUB_TOKEN')
    return discord_token, github_token

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    port = int(os.environ.get('PORT', '8000'))
    app.run(host='0.0.0.0', port=port)
