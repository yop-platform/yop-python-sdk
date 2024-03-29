# 打包发布


## 检查setup.py是否有错误
#python setup.py check

## 1.打包一个源代码的包
python3 setup.py clean --all && python3 setup.py check && python3 setup.py sdist build && python3 setup.py bdist_wheel --universal

python3 -m twine upload dist/*

# 发布

## 发布到
python -m pip install --user --upgrade setuptools wheel twine
python -m twine upload dist/*

# /Users/dreambt/Library/Python/2.7/bin/pytest -v
# pytest -v