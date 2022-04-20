import boto3
import json
import decimal
import datetime
import random
from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, request, jsonify

app = Flask(__name__)

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table = dynamodb.Table('parking_lot')

@app.route('/entry', methods=['POST'])
def Entry(plate_num,parking_lot):
    ticket_id = random.randint(1,1000000)
    time = datetime.datetime.now()
    response = table.put_item(
        Item={
            'plate_num': plate_num,
            'parking_lot': parking_lot,
            'time': time,
            'ticket_id': ticket_id
        }
    )
    return response

@app.route('/exit', methods=['POST'])
def exit(ticket_id):
    response = table.get_item(
        Key={
            'ticket_id': ticket_id
        }
    )
    time = response['Item']['time']
    price = price(time)
    return response

@app.route('/price', methods=['POST'])
def price(time):
    now = datetime.datetime.now()
    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    diff = now - time
    diff_min = diff.seconds/60
    price = diff_min/15*10
    return price

if __name__ == '__main__':
    app.run(debug=True)