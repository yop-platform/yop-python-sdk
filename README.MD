# yop-python-sdk

本软件是易宝开放平台（YOP）的 Python 语言 SDK，力争同时支持 Python2/3。

## Installation 安装方法

### Minimum Requirements 最小系统要求

- Python 3.5+
- Python 2.7+ (不能保证停止维护的Python版本有效，请参考https://www.python.org/doc/sunset-python-2/)

### Install from PyPI 从 PyPI 安装

## 生成虚拟环境

以 virtualenv 为例

```shell
pip install virtualenv
```

### For python3

```shell
# rm -rf ~/python3
/usr/bin/env /usr/bin/python3 -m virtualenv ~/python3
source ~/python3/bin/activate
```

## 安装 yop-python-sdk

### 从仓库安装最新版本

```shell
python -m pip install yop-python-sdk

# crypto 相关的报错如何解决
python -m pip uninstall crypto pycrypto pycryptodome yop-python-sdk
python -m pip install pycryptodome
```

### 从指定仓库安装指定的版本

```shell
python -m pip install --upgrade --index-url https://pypi.org/simple yop-python-sdk==4.2.6
```

### Install from source 从源码安装(不推荐)

```shell
python -m pip install git+https://github.com/yop-platform/yop-python-sdk.git
```

或者

```shell
git clone git@github.com:yop-platform/yop-python-sdk.git --depth=1
python setup.py install
```

## Samples 示例

### How to use 如何初始化 YopClient

采用默认配置文件：

```python
from client.yopclient import YopClient
client = YopClient()
```

采用指定的配置文件：

```python
from client.yopclient import YopClient
from client.yop_client_config import YopClientConfig
client = YopClient(YopClientConfig('config/yop_sdk_config_yours.json'))
```

Configure file Configure YopCredentials 采用配置文件中指定的 appKey 和私钥发起请求：

```python
api = '/rest/v1.0/pay/bank-limit/query'
params = {
    'merchantNo': '10000470992'
}
res = client.get(api=api, params=params)
```

Programmatically Configure YopCredentials 编码指定的 appKey 和私钥发起请求：

```python
api = '/rest/v1.0/pay/bank-limit/query'
params = {
    'merchantNo': '10000470992'
}
credentials = YopCredentials(appKey='<appKey>', cert_type='SM2|RSA2048', priKey='<私钥>')
res = client.get(api=api, params=params, credentials=credentials)
```

更多用法，请参考 test 目录下面的单元测试。

### ImportError: bad magic number in 'xxx'

```shell
rm -Rf **/*.pyc
```

## Contributing

Contributions are welcome! Check out the [Contribution Guide](CONTRIBUTING.md).

## License 协议

The code in this project is released under the [Apache 2.0](LICENSE).

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyop-platform%2Fyop-python-sdk.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyop-platform%2Fyop-python-sdk?ref=badge_large)
