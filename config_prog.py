import os
from app import Mine


# api_key='RPPtxiTDQ6atYnXq4wSgFL8I2c5t1r9fc7V26LpOalvWWbhBGTXDbZE3zdYrDoWs'
# api_secret='PmS9rwRysNbOfnZXcsO1OL2nNqppB2lrwIQRRx4ekvjKqvjJ4yf5J0hYo7wf4tQw'


get_crypto = Mine.query.filter_by(id=1).all()  # show list[<Minne:1>]
for crypto in get_crypto:
    minekey = crypto.key
    minesecret = crypto.secret
    print(minekey, minesecret)

minekey = os.getenv(minekey)
minesecret = os.getenv(minesecret)
