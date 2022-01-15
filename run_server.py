import sys
import os

from flask import Flask, request
from utils.anigitrest import Anigitrest


app = Flask('anigitbot_server')

@app.route('/')
async def serve():
    try:
        data = request.args
        discord_token, github_token = config()
        print(discord_token, github_token)
        channel_id = int(data.get('channel_id'))
        user = data.get('user')
        repository_name = data.get('repo')
        pr_number = int(data.get('pr'))
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
    port = int(os.environ.get('PORT', '8000'))
    app.run(host='0.0.0.0', port=port)
