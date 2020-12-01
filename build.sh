# 准备工作

## 确保您拥有setuptools并wheel 安装了最新版本
python3 -m pip install --user --upgrade setuptools wheel twine

# 打包

## 检查setup.py是否有错误
python3 setup.py check

## 1.打包一个源代码的包
python3 setup.py sdist build

## 2.也可以打包一个wheels格式的包
python3 setup.py bdist_wheel --universal

## 3.或者从setup.py位于的同一目录运行此命令：
python3 setup.py sdist bdist_wheel

# 发布

## 发布到
twine upload dist/*
