from flask_restful import abort, Resource, reqparse
from .goods import Goods
from . import db_session
from flask import jsonify

def abort_if_news_not_found(goods_id):
    session = db_session.create_session()
    goods = session.query(Goods).get(goods_id)
    if not goods:
        abort(404, message=f"Goods {goods_id} not found")

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('is_private', required=True, type=bool)
#parser.add_argument('is_published', required=True, type=bool)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('price', required=True)

class NewsResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(Goods).get(news_id)
        return jsonify({'goods': news.to_dict(
            only=('title', 'content', 'user_id', 'is_private', 'price'))})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(Goods).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})

class NewsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Goods).all()
        return jsonify({'goods': [item.to_dict(
            only=('title', 'content', 'user_id', 'price')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        news = Goods(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            #is_published=args['is_published'],
            is_private=args['is_private'],
            price=args['price']
        )
        session.add(news)
        session.commit()
        return jsonify({'success': 'OK'})