import flask

from . import db_session
from .goods import Goods

blueprint = flask.Blueprint(
    'goods_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/goods')
def get_goods():
    db_sess = db_session.create_session()
    news = db_sess.query(Goods).all()
    return flask.jsonify(
        {
            'goods':
                [item.to_dict(only=('title', 'content', 'price'))
                 for item in news]
        }
    )

@blueprint.route('/api/goods/<int:goods_id>', methods=['GET'])
def get_one_goods(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(Goods).get(news_id)
    if not news:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'goods': news.to_dict(only=(
                'title', 'content', 'user_id', 'is_private'))
        }
    )

@blueprint.route('/api/goods', methods=['POST'])
def create_goods():
    if not flask.request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in flask.request.json for key in
                 ['title', 'content', 'user_id', 'is_private', 'price']):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    news = Goods(
        title=flask.request.json['title'],
        content=flask.request.json['content'],
        user_id=flask.request.json['user_id'],
        is_private=flask.request.json['is_private'],
        price=flask.request.json['price']
    )
    db_sess.add(news)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})

@blueprint.route('/api/goods/<int:goods_id>', methods=['DELETE'])
def delete_goods(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(Goods).get(news_id)
    if not news:
        return flask.jsonify({'error': 'Not found'})
    db_sess.delete(news)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})