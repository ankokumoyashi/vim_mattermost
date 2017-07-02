import requests
import json

# 各種情報を入力

# TODO version変わったら考える


class Mattermost:
    def __init__(self, mattermost_url, login_id, password):
        api_version = 'api/v3'
        self.api_url = mattermost_url + api_version
        self.headers = self.login(login_id, password)

    def login(self, login_id, password):
        headers = {"Content-Type": "application/json"}
        data = {"login_id": login_id, "password": password}
        response = requests.post(self.api_url + '/users/login',
                                 json.dumps(data), headers)
        headers.update({
            "Authorization": "Bearer " + response.headers['Token'],
                         })
        return headers

    def get_team_posts(self, team_id):
        data = {"terms": "*", "is_or_search": True}
        response = self.post(self.api_url +
                             '/teams/' +
                             team_id +
                             '/posts/search', data).json()
        return response

    def get_team_id(self, team_name):
        response = self.get(self.api_url + '/teams/name/' + team_name)
        return response.json()['id']

    def get_channels(self, team_id):
        response = self.get(self.api_url + '/teams/' + team_id + '/channels/')
        channels = [{'id':item['id'], 'name':item['name']} for item in response.json()]
        return channels

    def get_posts(self, team_id, channels, offset, limit):
        response = [self.get_posts_channel(team_id, channel['id'], offset, limit) for channel in channels]
        return response


    def get_posts_channel(self, team_id, channel_id, offset, limit):
        response = self.get(self.api_url + '/teams/' + team_id +
                            '/channels/' + channel_id +
                            '/posts/page/' + str(offset) +'/'+ str(limit)).json()
        return response

    def post(self, url, data):
        response = requests.post(url,
                                 data=json.dumps(data),
                                 headers=self.headers)
        return response

    def get(self, url):
        response = requests.get(url, headers=self.headers)
        return response

if __name__ == "__main__":
    mattermost_url = 'http://localhost:8065/'
    login_id = 'ankokumoyashi'
    password = 'ankokumoyashi'
    team_name = 'ponkotsu'
    matter = Mattermost(mattermost_url, login_id, password)
    team_id = matter.get_team_id(team_name)
    channels = matter.get_channels(team_id)
    all_channel_post = matter.get_posts(team_id, channels, 0, 10)
    all_posts = [posts['posts'][post] for posts in all_channel_post for post in posts['order']]
