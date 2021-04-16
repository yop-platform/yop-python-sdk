# 准备工作

## 确保您拥有setuptools并wheel 安装了最新版本
# python3 -m pip install --user --upgrade setuptools wheel twine

# python -m pip uninstall crypto pycrypto pycryptodome yop-python-sdk
# python3 -m pip uninstall crypto pycrypto pycryptodome yop-python-sdk
# /Users/dreambt/Library/Python/2.7/bin/pip uninstall crypto pycrypto pycryptodome yop-python-sdk
# /Users/dreambt/Library/Python/2.7/bin/pip install pycryptodome

# 打包

source ~/yop-python-sdk/bin/activate
python setup.py clean --all

## 检查setup.py是否有错误
python setup.py check

## 1.打包一个源代码的包
python setup.py sdist build

## 2.也可以打包一个wheels格式的包
python setup.py bdist_wheel --universal

## 3.或者从setup.py位于的同一目录运行此命令：
# python setup.py sdist bdist_wheel

# 发布

## 发布到
# twine upload dist/*
python -m twine upload dist/*


# python -m pip install yop-python-sdk

# python -m pip install --upgrade --index-url https://pypi.org/simple yop-python-sdk==3.3.12


# /Users/dreambt/Library/Python/2.7/bin/pytest -v
# pytest -v