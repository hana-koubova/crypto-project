from datetime import datetime
from bson import ObjectId

from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify, send_file, send_from_directory, make_response
from flask_bootstrap import Bootstrap5
import os, json, requests
from werkzeug.exceptions import HTTPException

## WTFORMS

from flask_wtf.csrf import CSRFProtect, generate_csrf

## MondoDB related

from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient

## Inner Dependencies

from database import existing_crypto
from helper import check_for_symbol, get_crypto_list
from forms import AddCrypto

## App Initiation

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hellothisismysecretcrazykey9845947593884593@' #os.environ.get('FLASK_SECRET_KEY')

bootstrap = Bootstrap5(app)

## CSFP protection

csrf = CSRFProtect(app)
csrf.init_app(app)

@app.route("/", methods=['GET', 'POST'])
def index():
    all_currecies = existing_crypto.find({}).sort({'date_edited': -1})
    print('Hello hana')
    form = AddCrypto()
    #if form.validate_on_submit() and request.method == 'POST':
    if request.method == 'POST':
        print('Form validated')
        symbol = request.form['symbol']
        amount = request.form['amount']
        print('Form Accepted')

        ## Checking if symbol exists
        exist = check_for_symbol(symbol)
        print(exist)
        if exist != False:
            new_crypto = {
                'symbol': symbol,
                'amount': amount,
                'date_edited':  datetime.now(),
                'cryto_id': exist['id'],
                'name': exist['name']
            }
            print('Crypto Accepted')
            
            inserted_value = existing_crypto.insert_one(new_crypto)
            #print(inserted_value.inserted_id)

            return jsonify({
                'status': 'success',
                'symbol': new_crypto['symbol'],
                'amount': new_crypto['amount'],
                'date_edited': new_crypto['date_edited'].strftime('%B %d %Y, %H:%M'),
                'name': new_crypto['name'],
                'el_id': str(ObjectId(inserted_value.inserted_id)),
                'new_csrf_token': generate_csrf()
            })
        else:
            print('Crypto not accepted')
            return jsonify({'status': 'error', 'message': 'Invalid cryptocurrency symbol!'})

    return render_template('index.html',
                           form = form,
                           currencies = all_currecies)


@app.route('/delete_crypto/<crypto_id>', methods=['DELETE'])
def delete_crypto(crypto_id):
    
    try:
        # Find and delete the record by ID
        result = existing_crypto.delete_one({"_id": ObjectId(crypto_id)})
        
        if result.deleted_count == 1:
            print('Deleted')
            return jsonify({'status': 'success', 'message': 'Record deleted successfully!'})
        else:
            print('To delete Not found')
            return jsonify({'status': 'error', 'message': 'Record not found!'}), 404
    except Exception as e:
        print('To delete Error')
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route("/cyrpto_list", methods=['GET'])
def crypto_list():
    all_crypto = get_crypto_list()
    return render_template('crypto_list.html',
                           all_crypto = all_crypto)


if __name__ == "__main__":
    app.run(debug=True)