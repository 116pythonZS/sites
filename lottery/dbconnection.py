#!/usr/local/bin/pyenv python
# Created by carrot at 2017/9/10

"""
"""

import pymysql


def connectdb():
    _connection_ = pymysql.connect(host='127.0.0.1', user='hxl', password='198668', database="Lottery")
    return _connection_


dbcon = connectdb()


def main():
    print(dbcon)


if __name__ == "__main__":
    main()
