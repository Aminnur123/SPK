
from http import HTTPStatus
from flask import Flask, request, abort
from flask_restful import Resource, Api 
from models import cafe as CafeModel
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session

session = Session(engine)

app = Flask(__name__)
api = Api(app)        

class BaseMethod():

    def __init__(self):
        self.raw_weight = {'rating_minuman': 5, 'harga': 5, 'kualitas_pelayanan': 5, 'suasana': 5, 'rasa': 5}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(CafeModel.id_cafe, CafeModel.rating_minuman, CafeModel.harga, CafeModel.kualitas_pelayanan, CafeModel.suasana, CafeModel.rasa)
        result = session.execute(query).fetchall()
        print(result)
        return [{'id_cafe': tb_cafe.id_cafe, 'rating_minuman': tb_cafe.rating_minuman, 'harga': tb_cafe.harga, 'kualitas_pelayanan': tb_cafe.kualitas_pelayanan, 'suasana': tb_cafe.suasana, 'rasa': tb_cafe.rasa} for tb_cafe in result]

    @property
    def normalized_data(self):
        rating_minuman_values = []
        harga_values = []
        kualitas_pelayanan_values = []
        suasana_values = []
        rasa_values = []

        for data in self.data:
            rating_minuman_values.append(data['rating_minuman'])
            harga_values.append(data['harga'])
            kualitas_pelayanan_values.append(data['kualitas_pelayanan'])
            suasana_values.append(data['suasana'])
            rasa_values.append(data['rasa'])

        return [
            {'id_cafe': data['id_cafe'],
             'rating_minuman': data['rating_minuman'] / max(rating_minuman_values),
             'harga': min(harga_values) / data['harga'],
             'kualitas_pelayanan': data['kualitas_pelayanan'] / max(kualitas_pelayanan_values),
             'suasana': data['suasana'] / max(suasana_values),
             'rasa': data['rasa'] / max(rasa_values)
             }
            for data in self.data
        ]

    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class WeightedProductCalculator(BaseMethod):
    def update_weights(self, new_weights):
        self.raw_weight = new_weights

    @property
    def calculate(self):
        normalized_data = self.normalized_data
        produk = []

        for row in normalized_data:
            product_score = (
                row['rating_minuman'] ** self.raw_weight['rating_minuman'] *
                row['harga'] ** self.raw_weight['harga'] *
                row['kualitas_pelayanan'] ** self.raw_weight['kualitas_pelayanan'] *
                row['suasana'] ** self.raw_weight['suasana'] *
                row['rasa'] ** self.raw_weight['rasa']
            )

            produk.append({
                'id_cafe': row['id_cafe'],
                'produk': product_score
            })

        sorted_produk = sorted(produk, key=lambda x: x['produk'], reverse=True)

        sorted_data = []

        for product in sorted_produk:
            sorted_data.append({
                'id_cafe': product['id_cafe'],
                'score': product['produk']
            })

        return sorted_data


class WeightedProduct(Resource):
    def get(self):
        calculator = WeightedProductCalculator()
        result = calculator.calculate
        return result, HTTPStatus.OK.value
    
    def post(self):
        new_weights = request.get_json()
        calculator = WeightedProductCalculator()
        calculator.update_weights(new_weights)
        result = calculator.calculate
        return {'data': result}, HTTPStatus.OK.value
    

class SimpleAdditiveWeightingCalculator(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        result = {row['id_cafe']:
                  round(row['rating_minuman'] * weight['rating_minuman'] +
                        row['harga'] * weight['harga'] +
                        row['kualitas_pelayanan'] * weight['kualitas_pelayanan'] +
                        row['suasana'] * weight['suasana'] +
                        row['rasa'] * weight['rasa'], 2)
                  for row in self.normalized_data
                  }
        sorted_result = dict(
            sorted(result.items(), key=lambda x: x[1], reverse=True))
        return sorted_result

    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class SimpleAdditiveWeighting(Resource):
    def get(self):
        saw = SimpleAdditiveWeightingCalculator()
        result = saw.calculate
        return result, HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        saw = SimpleAdditiveWeightingCalculator()
        saw.update_weights(new_weights)
        result = saw.calculate
        return {'data': result}, HTTPStatus.OK.value


class cafe(Resource):
    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page < page_count:
            next_page = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next_page = None
        if page > 1:
            prev_page = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev_page = None
        
        if page > page_count or page < 1:
            abort(404, description=f'Halaman {page} tidak ditemukan.') 
        return {
            'page': page, 
            'page_size': page_size,
            'next': next_page, 
            'prev': prev_page,
            'Results': list[start:end]
        }

    def get(self):
        query = select(CafeModel)
        data = [{'id_cafe': tb_cafe.id_cafe, 'rating_minuman': tb_cafe.rating_minuman, 'harga': tb_cafe.harga, 'kualitas_pelayanan': tb_cafe.kualitas_pelayanan, 'suasana': tb_cafe.suasana, 'rasa': tb_cafe.rasa} for tb_cafe in session.scalars(query)]
        return self.get_paginated_result('tb_cafe/', data, request.args), HTTPStatus.OK.value


api.add_resource(cafe, '/tb_cafe')
api.add_resource(WeightedProduct, '/wp')
api.add_resource(SimpleAdditiveWeighting, '/saw')

if __name__ == '__main__':
    app.run(port='5005', debug=True)
