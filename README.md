# trading data

Uniquement pour Heroku (pas la cible runtime):
* requirements.txt / gunicorn
* runtime.txt
* Procfile


## install
'''
python -m pip install -r requirements.txt
'''

## init
'''
mongo_init_db.py
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