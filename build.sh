# 打包发布

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
python -m pip install --user --upgrade setuptools wheel twine
python -m twine upload dist/*

# /Users/dreambt/Library/Python/2.7/bin/pytest -v
# pytest -v