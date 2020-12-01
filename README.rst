# yop-python-sdk

## Installation 安装方法

### Minimum Requirements 最小系统要求

- Python 2.7+
- Python 3.2+

### Install from PyPI 从PyPI安装

python3 用户：

```
python3 -m pip install yop-python-sdk
```

### Install from source 从源码安装

```
git clone https://github.com/yop-platform/yop-python-sdk.git
python3 -m pip install ./yop-python-sdk
```

## Samples

### How to init YopClient 如何初始化 YopClient

采用默认配置文件：

```
from client.yopclient import YopClient
client = YopClient()
```

采用指定的配置文件：

```
from client.yopclient import YopClient
from utils.yop_config_utils import YopClientConfig
client = YopClient(YopClientConfig('config/yop_sdk_config_yours.json'))
```

Configure file Configure YopCredentials 采用配置文件中指定的 appKey 和私钥发起请求：

```
api = '/rest/v1.0/pay/bank-limit/query'
params = {
    'merchantNo': '10000470992'
}
res = client.get(api, params)
```

Programmatically Configure YopCredentials 编码指定的 appKey 和私钥发起请求：

```
api = '/rest/v1.0/pay/bank-limit/query'
params = {
    'merchantNo': '10000470992'
}
credentials = YopCredentials(appKey='<appKey>', priKey='<私钥>')
res = client.get(api, params, credentials)
```

更多用法，请参考 test 目录下面的单元测试。

# License 协议

This library is licensed under the Apache 2.0 License.
