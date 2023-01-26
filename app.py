from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import time
import sys
import requests
import threading
from binance.client import Client
# from config_prog import *
# from config import *
from tactical import SIGNALS_BY_SYMBOLS


# try:
#     from config import *
# except:
#     from config import *

app = Flask(__name__)
app.secret_key=b' MINEBOT:EASYEMA:order I DONT KNOW'
run = True
#################    DATABASE   ######################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mine.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mine.sql"  
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
with app.app_context():
    db = SQLAlchemy(app)
    db.init_app(app)
# db = SQLAlchemy(app)


class Mine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    secret = db.Column(db.String(64), unique=True, nullable=False)  
   
    def __repr__(self):
        # return '<mine %r>' % self.id
        return f'<Mine:{self.id}>'



class SIGNALS_MORNITORING(threading.Thread):
    
    def __init__(self,coins_list = []):
        self.need_to_break = False
        self.coins_list = []
    
    def job(self):
        print("CHECKING FOR SIGNALS PLEASE WAITS")

        # coin_list = ["BTCUSDT","ETHUSDT","BCHUSDT","LTCUSDT","DOGEUSDT","DOTUSDT","ADAUSDT","BNBUSDT"]
        # ADA,SOL,ATOM,COS
        coin_list = ["SOLBNB","COSBNB","OPBNB","RSRBNB","ATOMBNB","OCEANBNB","XRPBNB"]
        for coin in coin_list:
            print(coin)
            r = SIGNALS_BY_SYMBOLS(coin)
            if r == "BUY":
                print("BUY NOW")
            
            elif r == "SELL":
                print("SELL NOW")
            
            else:
                print("NO SIGNALS")
    
    def run(self):
        print(self.need_to_break)
        while True:
            if not self.need_to_break:
                print("=======SCANNOW=======")
                self.job()
                time.sleep(10)
                print("=====================")
            
            elif not self.need_to_break:
                print("BOT STOP NOW")
            
            else:
                print("BOT KILLED")
                break
    
    def stop(self):
        print("Stop Signals")
        self.need_to_break = True
    
    def resume(self,command):
        print("Resume Signals")
        self.need_to_break = command

    # def userInfo(self):
    #     client = Client(mine_key,mine_secret,app.secret_key)
    #     info = client.get_account()
    #     print(info)
    



SM = SIGNALS_MORNITORING()
SM_t = threading.Thread(target=SM.run,daemon=True)

@app.route("/<START>", methods=['POST'])
def stop_app(START):
    if START=="START":
        try:
            SM_t.start()
        except:
            SM.resume(command=False)
            SM.run()            
        # SM_t.start()
    else:
        SM.stop()

    # return "ok"
    # return render_template('index.html')
    return redirect('/minebot')


# @app.route("/<STOP>",methods=['GET','POST'])
# def stop(STOP):
#     if STOP == "STOP":
#         # try:
#         #     SM.stop
#         # except:
#         #     SM_t.start()
#         #     SM.resume(command=True)            
#         # else:
#         #     SM.run
#         try:
#          SM_t.run
#             # requests.post(url="http://127.0.0.1:5000/START")
#         except:
#             SM.resume(command=True)
#             SM.stop()
#         else:            
#             SM.run()
#             # requests.post(url="http://127.0.0.1:5000/STOP")
#             return render_template('index.html')
#             # return redirect('/minebot')


# @app.route("/<STOP>", methods=['GET','POST'])
# def start_app(STOP):
#     if STOP=="STOP":
      
#         try:
#             SM_t.start()
    
#         except:
#             SM.resume(command=True)
#             SM.stop()
#             # SM_t.start()
#     else:
        
#         SM.start()
    
    
#     # return "ok"

    
#     return render_template('/index.html')
    


@app.route("/",methods=['GET','POST'])
# def loading():
#     return render_template('loading.html')

def test_signals():    
    if request.method == "POST":
        msg = request.data.decode("utf-8")

        """
        MINEBOT : EASY EMA: order
        {{strategy.order.action}}
        @ {{strategy.order.contracts}}
        filled on {{ticker}}.
        New strategy position is
        {{strategy.position_size}}
        """
        #สรุปว่า BTCUSDT ขาย
        #if symbol , signals
            #PlaceSELL
        #else
            #PlaceBUY
        
        return "This is buying signals"

    else:
        # return "กรุณานำ Link ไปใส่ไว้ที่ Webhook Tradingview"
         return render_template('loading.html')

@app.route("/<pairname>")
def pair_signals(pairname):

    """
    binance , Talibs , matplotlib
    """
    return "This is {} buying signals".format(pairname)

@app.route("/minebot")
def index():
    time.sleep(2)
    # return 'Hello'
    # get_crpto = Mine.query.order_by(Mine.id).all() # show all data
    ## CRYPTO ##
    get_crypto = Mine.query.filter_by(id=1).all() # show list[<Minne:1>]
    for crypto in get_crypto:                
        minekey = crypto.key
        minesecret = crypto.secret
        # print(crypto.key,crypto.secret)
        # print(minekey,minesecret)        
    # client = Client(mine_key, mine_secret)
    # info = client.get_account()
    # print(info)

    return render_template('index.html',posts=get_crypto)

@app.route("/config")
def config():
    userInfo = Client
    return render_template('config.html')
# @app.route('/')
# def index():
# 	return 'Hello'

@app.route("/showdata")
def showdata():
    show_data = Mine.query.order_by(Mine.id).all()    
    return render_template('showdata.html',posts=show_data)

@app.route("/addData", methods=["POST"])
def add_data():
    db.create_all()    
    get_key = request.form.get('apikey')
    get_secret = request.form.get('apisecret')
    mineDB = Mine(key=get_key,secret=get_secret)
    try:
        db.session.add(mineDB)
        db.session.commit()
        # return redirect('/config')
        return redirect('/minebot')
    except:
        return 'Add Data Success '
        # return redirect('/minebot')

@app.route('/update/<int:id>',methods=['GET','POST'])
def update_data(id):
    data_to_update = Mine.query.get_or_404(id)
    
    if request.method=='POST':
        data_to_update.key = request.form['apikey']
        data_to_update.secret = request.form.get('apisecret')

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'unable to update'
    else:
        return render_template('update.html',posts=data_to_update)

@app.route('/delete/<int:id>')
def delete_data(id):
    data_to_delete = Mine.query.get_or_404(id)

    try:
        db.session.delete(data_to_delete)
        db.session.commit()
        # return redirect('/')
        return redirect('/showdata')
    except:
        return 'There was a problem deleting this article'
        # return redirect('/showdata')




if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)    
        