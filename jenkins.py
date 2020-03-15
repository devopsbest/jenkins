
import jenkins

job_name = "engage-ec-envSelector"

"""
Author: Anderson
公众号： python爱好部落
QQ群：643285853
"""


class Jenkins_Api:
    def __init__(self, username='m', password='G'):
        self._url = 'http://10.128.10.10:8080/'
        self._username = username
        self._password = password
        self.get_server = jenkins.Jenkins(self._url, username=self._username, password=self._password)

    def get_version(self):
        return self.get_server.get_version()

    def get_jobs(self):
        return self.get_server.get_jobs()

    def get_jobs_count(self):
        return self.get_server.jobs_count()

    def get_job_config(self, job_name):
        return self.get_server.get_job_config(job_name)

    def create_job(self, job_name, config_xml):
        return self.get_server.create_job(job_name, config_xml)

    def copy_job(self, job_name, new_job_name):
        return self.get_server.copy_job(job_name, new_job_name)

    def delete_job(self, job_name):
        return self.get_server.delete_job(job_name)

    def build_job(self, job_name):
        return self.get_server.build_job(job_name)

    def get_job_info(self, job_name):
        return self.get_server.get_job_info(job_name)

    def get_job_number(self, job_name):
        return self.get_server.get_job_info(job_name)['lastCompletedBuild']['number']

    def get_build_info(self, job_name, number):
        return self.get_server.get_build_info(job_name, number)

    def get_views(self):
        return self.get_server.get_views()


import jsonpath

api = Jenkins_Api()

number = api.get_job_number(job_name)
print("The last number is {}".format(number))

build = api.get_build_info(job_name, number)
print(build['url'])

branch = jsonpath.jsonpath(build, '$.actions..value')
author = jsonpath.jsonpath(build, '$.actions..userName')
print(branch)
print(author)

console = build['url'] + 'console'

import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
r = requests.get(console, headers=headers)
content = r.text
soup = BeautifulSoup(content, 'lxml')

url = ""
for x in soup.find_all('a', href=re.compile('alphaqr')):
    url = x

if url != "":

    print("...start to open url...")
    reg = re.compile(">(.*?)<")
    url_final = reg.search(str(url))
    qrcode_url = url_final.group(1)

    import webbrowser as web

    web.open(qrcode_url, new=0, autoraise=True)  # new:0/1/2 0：同一浏览器窗口打开 1：打开浏览器新的窗口，2：打开浏览器窗口新的tab
    #                                                         #autoraise=True:窗口自动增长
    # web.open_new("")
    # web.open_new_tab("")
else:
    print("no url found!")
