from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from forms.search_form import *
from data import sessions
from data.model_container import *


ADRESS = '127.0.0.1'
PORT = 8080
DB_PATH = 'databases/musical.sqlite'
TEXTS_PATH = 'texts/'
TEXT_SHORTVIEW = 4  # сколько строчек показываем на превью в /home
WORDS_IN_LINE = 10
REGISTER_FAILED = 'Товарищ! Проверьте правильность введенных данных!'
ERROR_MESSAGE = 'Простите, товарищ! Мы не смогли обработать этот запрос. Даешь текст ошибки, как в детстве!\n'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def get_artist_by_track(track, session):
    return session.query(User).filter(User.id == track.artist_id).first().name


@login_manager.user_loader
def load_user(user_id):
    db_sess = sessions.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def start_page():
    form = SearchForm()
    result = []
    artists = dict()
    if form.validate_on_submit():
        request = form.query.data.lower()
        session = sessions.create_session()
        result = session.query(Track).filter(Track.name.like(f'%{request}%'))
        artists = {track: get_artist_by_track(track, session) for track in result}
    return render_template('start.html', form=form, results=result, artists=artists)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    message = 0
    if form.validate_on_submit():
        user = sessions.create_session().query(User).filter(User.email == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/home')
        else:
            message = REGISTER_FAILED
    return render_template('login.html', form=form, message=message)


@app.route('/sign', methods=['GET', 'POST'])
def signin():
    form = SignForm()
    message = 0
    if form.validate_on_submit():
        sesssion = sessions.create_session()
        user = User()
        if form.password.data == form.check_password.data and not sesssion.query(User).filter(User.email
                                                                                              == form.login.data).first():
            user.name, user.email = form.name.data, form.login.data
            user.create_password(form.password.data)
            sesssion.add(user)
            sesssion.commit()
            login_user(user)
            return redirect('/home')
        else:
            message = REGISTER_FAILED
    return render_template('signin.html', form=form, message=message)


@app.route('/home')
@login_required
def home():
    session = sessions.create_session()
    tracks = session.query(Track).filter(Track.artist_id == current_user.id)
    texts = dict()
    for track in tracks:
        try:
            texts[track] = ''.join(open(TEXTS_PATH + str(track.id) + '.txt', 'r').readlines()[:TEXT_SHORTVIEW])
        except Exception as e:
            texts[track] = ERROR_MESSAGE + str(e)
    return render_template('home.html', tracks=tracks, texts=texts)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    is_new = False
    form = EditForm()
    session = sessions.create_session()
    track = session.query(Track).filter(Track.id == id).first()
    if not track:
        track, is_new = Track(), True
    if form.validate_on_submit():
        track.name = form.name.data.lower()
        if is_new:
            track.artist_id = current_user.id
            session.add(track)
        session.commit()
        with open(TEXTS_PATH + str(track.id) + '.txt', 'w') as file:
            text = str(form.text.data).split()
            file.write('\n'.join(list(' '.join(text[i:i + WORDS_IN_LINE])
                                      for i in range(0, len(text), WORDS_IN_LINE))))
        return redirect('/home')
    try:
        form.name.data = track.name
        form.text.data = ' '.join(open(TEXTS_PATH + str(track.id) + '.txt', 'r').readlines())
    except Exception:
        form.text.data, form.name.data = '', ''
    return render_template('edit.html', form=form, id=id)


@app.route('/lyric/<int:id>')
def lyric(id):
    session = sessions.create_session()
    track = session.query(Track).filter(Track.id == id).first()
    artist = get_artist_by_track(track, session)
    text = open(TEXTS_PATH + str(id) + '.txt', 'r').readlines()
    return render_template('lyric.html', name=track.name, artist=artist, text=text)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


def main():
    sessions.global_init(DB_PATH)
    session = sessions.create_session()
    session.commit()
    app.run(ADRESS, PORT)


if __name__ == '__main__':
    main()
