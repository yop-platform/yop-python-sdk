# -*- coding: utf-8 -*-

import sys
sys.path.append("./")
import pytest
from client.yopclient import YopClient
from utils.yop_config_utils import YopClientConfig


def pytest_addoption(parser):
    '''
    添加命令行参数 --env
    '''

    parser.addoption(
        "--env", action="store", default="prod", help="browser option: local, qa, pro"
    )


@pytest.fixture(scope='session')
def client(request):
    env = request.config.getoption("--env")
    if env == "local":
        print('初始化本地环境的 Yop Client')
        client = YopClient(YopClientConfig('config/yop_sdk_config_local.json'))
    elif env == "qa":
        print('初始化QA环境的 Yop Client')
        client = YopClient(YopClientConfig('config/yop_sdk_config_qa.json'))
    else:
        print('初始化生产环境的 Yop Client')
        client = YopClient()
    return client
