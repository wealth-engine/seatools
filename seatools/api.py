import os
import json
import requests

from seatools.common import logger
from seatools.common import judgment_login

logger = logger()


class BaseAPI:

    def __init__(self):
        self.url = "https://oss.wealthengine.cn/api2"
        self.token = None

    def connect(self, username, password):
        userinfo = {
            "username": username,
            "password": password
        }
        url = f'{self.url}/auth-token/'
        res = requests.post(url, data=userinfo)
        if res.status_code == 200:
            data = json.loads(res.text)
            self.token = data.get("token")
        else:
            raise Exception("账号或密码错误")

    @property
    @judgment_login
    def headers(self):
        headers = {
            "Authorization": f"Token {self.token}"
        }
        return headers

    def get(self, url):
        result = requests.get(url, headers=self.headers)
        data = json.loads(result.text)
        return data

    def post(self, url, **kwargs):
        result = requests.post(url, headers=self.headers, **kwargs)
        try:
            data = json.loads(result.text)
        except Exception as e:
            return result.text
        return data

    def delete(self, url, **kwargs):
        result = requests.delete(url, headers=self.headers, **kwargs)
        if result.status_code != 200:
            return False
        return result


class RepoAPI(BaseAPI):
    def repos_list(self):
        """
        获取所有 libraries
        """
        url = f'{self.url}/repos/?type=group'
        data = self.get(url)
        return data

    def create_repo(self, repo_name):
        data = self._get_repo_by_name(repo_name)
        if data:
            return data[0]
        url = f'{self.url}/groups/3/repos/'
        repo_name = {"name": repo_name}
        create_info = self.post(url, data=repo_name)
        return create_info

    def get_repo_by_name(self, name):
        """
        通过 name 查找 repo
        return: dict
        """
        url = f'{self.url}/repos/?nameContains={name}'
        data_list = self.get(url)
        if not data_list:
            raise Exception(f"{name} is not exist or you don't have access")
        return data_list[0]

    def get_repo_by_id(self, repo_id):
        url = f'{self.url}/repos/{repo_id}'
        data = self.get(url)
        return data

    def get_repo_commit_info(self, name):
        """
        获取某个 library 的所有提交信息
        """
        repo = self.get_repo_by_name(name)
        url = f'{self.url}/repos/{repo.get("id")}/history/'
        commit_info_list = self.get(url)
        return commit_info_list['commits']

    def get_dir(self, repo_id):
        """
        获取 repo 下的所有文件
        """
        url = f"{self.url}/repos/{repo_id}/dir/"
        file_list = self.get(url)
        return file_list

    def _get_repo_by_name(self, name):
        url = f'{self.url}/repos/?nameContains={name}'
        data_list = self.get(url)
        return data_list


class FileAPI(RepoAPI):

    def get_file(self, repo_id, file_name, to_folder):
        url = f'{self.url}/repos/{repo_id}/file/?p=/{file_name}'
        file_link = requests.get(url, headers=self.headers).text
        file = requests.get(eval(file_link), headers=self.headers)

        if not os.path.exists(to_folder):
            raise Exception(f"{to_folder} is not exits")

        with open(f"{to_folder}/{file_name}", 'wb') as file_obj:
            file_obj.write(file.content)

    def get_file_detail(self, repo_id, file_name):
        url = f'{self.url}/repos/{repo_id}/file/detail/?p={file_name}'
        detail_info = self.get(url)
        return detail_info

    def download_file(self, repo_id, file_name, to_folder):
        """
        下载或者更新单个文件
        """
        local_file_path = os.path.join(to_folder, file_name)
        if os.path.exists(local_file_path):
            remote_file_mtime = self.get_file_detail(repo_id, file_name).get("mtime")
            local_file_path_mtime = os.path.getmtime(local_file_path)
            if remote_file_mtime <= local_file_path_mtime:
                return

        self.get_file(repo_id, file_name, to_folder)

    def download_files(self, repo_name, to_folder):
        repo_id = self.get_repo_by_name(repo_name).get("id")
        file_list = self.get_dir(repo_id)
        for file_info in file_list:
            name = file_info.get("name")
            self.download_file(repo_id, name, to_folder)

    def upload_folder(self, folder, repo_id):
        url = f'{self.url}/repos/{repo_id}/upload-link/?p=/'
        upload_link = self.get(url)

        files = [("parent_dir", "/")]
        if not os.path.exists(folder):
            raise Exception(f"{folder} is not exist")

        folder_files = os.listdir(folder)

        for file_name in folder_files:
            file_path = os.path.join(folder, file_name)
            if not os.path.exists(file_path):
                raise Exception(f"{file_path} is not exist")
            file_tuple = ("file", open(file_path, 'rb'))
            files.append(file_tuple)
        upload_res = self.post(upload_link, files=files)
        # print(f"{folder} uploaded successfully")
        logger.info(f"{folder} uploaded successfully")
        return upload_res

    def delete_folder(self, repo_name):
        repo_list = self._get_repo_by_name(repo_name)
        if not repo_list:
            raise Exception(f"{repo_name} is not exists")
        repo_id = repo_list[0].get("id")
        del_url = f"{self.url}/repos/{repo_id}/"
        res = self.delete(del_url)
        logger.info(f"{repo_name} delete is success")
        return res

