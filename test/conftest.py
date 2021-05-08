# -*- coding: utf-8 -*-

import pytest
from client.yopclient import YopClient
from client.yop_client_config import YopClientConfig


def pytest_addoption(parser):
    '''
    添加命令行参数 --env
    '''

    parser.addoption(
        "--env", action="store", default="prod", help="browser option: local, qa, prod"
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
        config_file = 'config/yop_sdk_config_{}_{}.json'.format(cert_type, env)
    elif env == "qa":
        print('初始化QA环境的 Yop Client')
        config_file = 'config/yop_sdk_config_{}_{}.json'.format(cert_type, env)
    else:
        print('初始化生产环境的 Yop Client')
        config_file = 'config/yop_sdk_config_{}_{}.json'.format(cert_type, env)

    print('config_file:{}'.format(config_file))
    clientConfig = YopClientConfig(config_file)
    client = YopClient(clientConfig, cert_type, env)
    return client
