from flask import Flask, render_template, redirect, request, abort, jsonify
from data import db_session
from data.users import User
from data.goods import Goods
from data.corzina import Corzina
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.goods import NewsForm
from forms.user import UsersForm
from data import goods_api
from flask import make_response
from flask_restful import Api
from data import goods_resources
from sqlalchemy import desc


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/market.db")
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route("/", methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods).order_by(desc('id'))
    return render_template("index.html", goods=goods)

@app.route("/up")
def up():
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods).order_by(desc('id'))
    return render_template("index.html", goods=goods)

@app.route("/down")
def down():
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods)
    return render_template("index.html", goods=goods)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/corzina')
@login_required
def corzina():
    summa = 0
    db_sess = db_session.create_session()
    users = db_sess.query(Corzina)
    for elem in users:
        summa += int(elem.price)
    return render_template('corzina.html', users=users, summa=summa)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/poisk/<string:poisk>', methods=['GET', 'POST'])
def poisk(poisk):
    form = UsersForm()
    if form.validate_on_submit():
        return redirect(f'/poisk/{form.poisk.data}')
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods).filter(Goods.title.like(f'%{poisk}%'))
    return render_template("poisk.html", goods=goods, form=form, poisk=poisk)

@app.route('/poisk_poisk', methods=['GET', 'POST'])
def poisk_poisk():
    form = UsersForm()
    if form.validate_on_submit():
        return redirect(f'/poisk/{form.poisk.data}')
    return render_template('poisk_poisk.html', form=form)


@app.route('/profile_edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = UsersForm()
    if form.validate_on_submit():
        users = User()

        users.name = form.name.data
        users.email = form.email.data
        users.image = form.image.data
        db_sess = db_session.create_session()
        news = db_sess.query(User).filter(User.name == current_user.name
                                           ).first()
        if news:
            if users.name:
                news.name = form.name.data
            else:
                news.name = current_user.name
            if users.email:
                news.email = form.email.data
            if users.image:
                news.image = f'/static/img/{form.image.data}'
            db_sess.commit()
        return redirect('/profile')
    return render_template('profile_edit.html',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/submit')
@login_required
def submit():
    return render_template('submit.html')


@app.route('/goods',  methods=['GET', 'POST'])
@login_required
def add_goods():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = Goods()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        news.price = form.price.data
        news.image = f'/static/img/{form.image.data}'
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('goods.html', title='Добавление товара',
                           form=form)

@app.route('/goods/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_goods(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(Goods).filter(Goods.id == id,
                                          Goods.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.price.data = news.price
            form.image.data = news.image
            form.content.data = news.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(Goods).filter(Goods.id == id,
                                          Goods.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.price = form.price.data
            if form.image.data:
                news.image = f'/static/img/{form.image.data}'
            db_sess.commit()
            news = db_sess.query(Goods).filter(Goods.id == id,
                                               Goods.user == current_user
                                               )
            return render_template('wide_good.html',
                                   form=form, news=news
                                   )

        else:
            abort(404)

    return render_template('goods.html',
                           title='Редактирование товара',
                           form=form
                           )

@app.route('/goods_photo/<int:id>', methods=['GET', 'POST'])
def goods_photo(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Goods).filter(Goods.id == id).first()
    image = news.image
    id = news.id
    return render_template('goods_photo.html', image=image, id=id)

@app.route('/user_photo/<int:id>', methods=['GET', 'POST'])
def user_photo(id):
    db_sess = db_session.create_session()
    news = db_sess.query(User).filter(User.id == id).first()
    image = news.image
    return render_template('user_photo.html', image=image)

@app.route('/wide_good/<int:id>', methods=['GET', 'POST'])
def wide_good(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Goods).filter(Goods.id == id)
    for item in news:
        id = item.user_id
    user = db_sess.query(User).filter(User.id == id).first()
    return render_template('wide_good.html', news=news, name=user.name, id=user.id)

@app.route('/user_profile/<int:id>', methods=['GET', 'POST'])
def user_profile(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    news = db_sess.query(Goods).filter(Goods.user_id == id)
    return render_template('user_profile.html', user=user, news=news)

@app.route('/my_goods', methods=['GET', 'POST'])
def my_goods():
    db_sess = db_session.create_session()
    news = db_sess.query(Goods).filter(Goods.user_id == current_user.id)
    return render_template('my_goods.html', news=news)

@app.route('/good_success/<int:id>', methods=['GET', 'POST'])
@login_required
def good_success(id):
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods).filter(Goods.id == id).first()
    goods.is_private = 1
    news = Corzina()
    news.id = goods.id
    news.user_id = goods.user_id
    news.title = goods.title
    news.content = goods.content
    news.price = goods.price
    news.image = goods.image
    db_sess.add(news)
    db_sess.commit()
    return render_template('good_success.html', title=goods.title, id=id)

@app.route('/corzina_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def corzina_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Corzina).filter(Corzina.id == id).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    goods = db_sess.query(Goods).filter(Goods.id == id).first()
    goods.is_private = 0
    db_sess.commit()
    return render_template('corzina_delete.html', title=news.title, id=id)

@app.route('/goods_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def goods_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Goods).filter(Goods.id == id,
                                      Goods.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

"""@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)"""
def main():
    api = Api(app)
    #app.register_blueprint(news_api.blueprint)
    # для списка объектов
    api.add_resource(goods_resources.NewsListResource, '/api/goods')

    # для одного объекта
    api.add_resource(goods_resources.NewsResource, '/api/goods/<int:news_id>')
    app.run(port=8080, host='127.0.0.1')

if __name__ == '__main__':
    main()
