import os
import sys
import time
import datetime
sys.path.insert(0, os.path.dirname(__file__))
from operator import itemgetter
from mattermost import Mattermost
import neovim

#mattermost_url = 'http://masala.soft.fujitsu.com/'
#login_id = 'g.inatomi@jp.fujitsu.com'
#password = 'nin10gen'
#team_name = 'fjspf'

mattermost_url = 'http://localhost:8065/'
login_id = 'ankokumoyashi'
password = 'ankokumoyashi'
team_name = 'ponkotsu'

@neovim.plugin
class Handler():
    def __init__(self, vim=None):
        self.vim = vim
        self.buf = vim.current.buffer
        self.matter = Mattermost(mattermost_url, login_id, password)
        self.team_id = self.matter.get_team_id(team_name)
        self.uid2name = self.make_uid2name(self.matter.get_users())

    @neovim.function('Mattermost')
    def mattermost(self, args=None):
        channels = self.matter.get_channels(self.team_id)
        self.cid2name = self.make_cid2name(channels)
        self.id2time = self.get_last_post_time(channels)
        self.updater()

    def updater(self):
        while True:
            time.sleep(1)
            channels = self.matter.get_channels(self.team_id)
            updated_channels = self.check_post_time(channels)
            self.id2time = self.get_last_post_time(channels)
            if updated_channels:
                all_channel_post = self.matter.get_posts(self.team_id, updated_channels, 0, 1)
                all_posts = [posts['posts'][post] for posts in all_channel_post for post in posts['order']]
                all_posts.sort(key=itemgetter('create_at'), reverse = True)
                [self.buf_write(post) for post in all_posts]

    def buf_write(self, content):
        self.buf.append(str(datetime.datetime.fromtimestamp(content['create_at']/1000.0)))
        self.buf.append(self.cid2name[content['channel_id']] + ':' + self.uid2name[content['user_id']])
        [self.buf.append(line) for line in content['message'].split('\n')]
        self.buf.append('')
        return 1

    def make_uid2name(self, users):
        return {user_id: users[user_id]['username'] for user_id in list(users.keys())}

    def make_cid2name(self, channels):
        return {channel['id']: channel['display_name'] for channel in channels}

    def get_last_post_time(self, channels):
        return {channel['id']: channel['last_post_at'] for channel in channels}

    def check_post_time(self, channels):
        channels = [channel for channel in channels if channel['last_post_at'] > self.id2time[channel['id']]]
        return channels



if __name__ == '__main__':
    hand = Handler()
    hand.mattermost()
