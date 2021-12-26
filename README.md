# trading data

## install
'''
python -m pip install -r requirements.txt
'''
ou
'''
cat requirements.txt | xargs -n 1 pip install
'''

### powershell

Get-ChildItem Env:PYTHONPATH

$env:PYTHONPATH = ${pwd}

## start | stop mongodb service

### on windows
start powershell as admin
'''
net start|stop MongoDB
'''

## init
'''
main_mongo_init_db.py
'''

## run

Flask running on http://127.0.0.1:5000/

## doc
[https://docs.python-guide.org/writing/structure/](https://docs.python-guide.org/writing/structure/)

[https://python-binance.readthedocs.io/en/latest/market_data.html](https://python-binance.readthedocs.io/en/latest/market_data.html)

[https://technical-analysis-library-in-python.readthedocs.io/en/latest/](https://technical-analysis-library-in-python.readthedocs.io/en/latest/)

[https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)

[https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb](https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb)

[https://docs.mongodb.com/manual/reference/mongo-shell/](https://docs.mongodb.com/manual/reference/mongo-shell/)

'''
& 'C:\Program Files\MongoDB\Server\5.0\bin\mongo.exe'
'''

db.ohlc.find({exchange: 'binance', pair: 'ETHEUR', interval: '1h'}).sort( { timestamp: -1 } ).limit(1)

db.ohlc.find({exchange: 'kucoin', pair: 'ETH-USDT', interval: '2hour'}).sort( { timestamp: -1 } ).limit(20)

db.ohlc.find({exchange: 'binance', pair: 'BTCUSDT', interval: '4h'}).sort( { timestamp: -1 } ).limit(1)

db.ohlc.aggregate({$group: {_id: {"exchange": "$exchange", "pair": "$pair", "interval": "$interval"}, count:{"$sum": 1}}})

# raspberry pi
install from source python3.10, then:
'''
sudo ln -s /usr/share/pyshared/lsb_release.py /usr/local/lib/python3.10/site-packages/lsb_release.py
'''