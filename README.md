# seatools

seatools 是一个在 seafile 中下载文件的程序
## 环境准备
```bash
pip install seatools -U -i http://115.28.185.117:8181/repository/mypypi/simple --trusted-host 115.28.185.117:8181
```

## 使用示例

- 上传文件夹

```python
from seatools.api import FileAPI

upload = FileAPI()
upload.connect(username="xxxxx@xxx.xx", password="xxxxxxx")

# repo_name: 为 seafile 中的目录名称
repo = upload.create_repo(repo_name="test_hxc1")
repo_id = repo.get("id")
upload.upload_folder(r"\var\mnt\data", repo_id)
```

- 删除目录

```python
from seatools.api import FileAPI

upload = FileAPI()
upload.connect(username="xxxxx@xxx.xx", password="xxxxxxx")

# repo_name: seafile 中的目录名
upload.delete_folder(repo_name="repo_name")
```

- 下载文件

```python
from seatools.api import FileAPI

upload = FileAPI()
upload.connect(username="xxxxx@xxx.xx", password="xxxxxxx")

# repo_name: seafile 中的文件名 repo_name
# to_folder: 存放到本地的目录
upload.download_files(repo_name="repo_name", to_folder=r"\var\mnt\data")
```
