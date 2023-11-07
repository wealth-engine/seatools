"""
 @Author: hanlearned
 @Email: hanlearned99@gmail.com
 @FileName: test_api.py
 @DateTime: 2023/8/9 15:50
 @SoftWare: PyCharm
"""
from seatools.api import FileAPI


class TestApi:
    def setup_class(self):
        self.upload = FileAPI()
        self.upload.connect(username="hanxuecheng@wealthengine.cn", password="4455678Hxc")

    def test_upload(self):
        repo_id = self.upload.create_repo("test_upload").get("id")
        self.upload.upload_folder(r".\upload_file", repo_id)

    def test_download(self):
        pass

    def test_del_folder(self):
        pass

