# -*- coding: utf-8 -*-

from client.yop_client_config import YopClientConfig
from client.yopclient import YopClient
import pytest
import sys
sys.path.append("./")


def pytest_addoption(parser):
    '''
    添加命令行参数 --env
    '''

    parser.addoption(
        "--env", action="store", default="prod", help="browser option: local, qa, pro"
    )
    parser.addoption(
        "--cert-type", action="store", default="rsa", help="browser option: sm, rsa"
    )


@pytest.fixture(scope='session')
def client(request):
    env = request.config.getoption("--env")
    cert_type = request.config.getoption("--cert-type")
    if env == "local":
        print('初始化本地环境的 Yop Client')
        config_file = 'config/yop_sdk_config_{}_local.json'.format(cert_type)
    elif env == "qa":
        print('初始化QA环境的 Yop Client')
        config_file = 'config/yop_sdk_config_{}_qa.json'.format(cert_type)
    else:
        print('初始化生产环境的 Yop Client')
        config_file = 'config/yop_sdk_config_{}_default.json'.format(cert_type)

    print('config_file:{}'.format(config_file))
    clientConfig = YopClientConfig(config_file)
    client = YopClient(clientConfig)
    return client
