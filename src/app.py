from flask import Flask, abort, jsonify, request

from database import init_db, db
from model.models import User, UserSchema, List, ListSchema

from sqlalchemy import func

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    init_db(app)
    return app


app = create_app()

if __name__ == '__main__':
    app.run()


@app.route('/users')
def hello():
    results = User.query.all()
    if results is None:
      return abort(404)
    return jsonify({'status': 'ok', 'users': UserSchema(many=True).dump(results)})


@app.route('/user/<int:id>')
def user(id):
    user = User.query.get_or_404(id)
    return jsonify({'status': 'ok', 'users': UserSchema().dump(user)})


@app.route('/lists')
def all_list():
    results = List.query.all()
    if results is None:
      return abort(404)
    return jsonify({'status': 'ok', 'lists': ListSchema(many=True).dump(results)})


@app.route('/list', methods=['POST'])
def new_list():
    data = request.get_json()
    if data is None:
      return abort(404)
    list = List(data['name'], data['description'], data['content'], 2)
    db.session.add(list)
    db.session.commit()
    return jsonify({'status': 'ok', 'list': ListSchema().dump(list)})


@app.route('/list/<int:id>', methods=['POST', 'GET'])
def list(id):
    list = List.query.get(id)
    if list is None:
        return abort(404)
    if request.method == 'GET':
        return jsonify({'status': 'ok', 'list': ListSchema().dump(list)})
    data = request.get_json()
    if data is None:
      return abort(404)
    list.update_dict(data)
    db.session.commit()
    return jsonify({'status': 'ok', 'list': ListSchema().dump(list)})

@app.route('/list/<int:id>/<int:item>')
def list_item(id, item):
    list = List.query.get(id)
    if list is None:
        return abort(404)
    if request.method == 'GET':
        return jsonify({'status': 'ok', 'list': list.content[item]})
    data = request.get_json()
    if data is None:
      return abort(404)
    list.update_dict(data)
    db.session.commit()
    return jsonify({'status': 'ok', 'list': ListSchema().dump(list)})


@app.route('/list/<int:id>/<int:item>/<int:check>', methods=['POST', 'GET'])
def list_item_check(id, item, check):
    list = List.query.get(id)
    if list is None:
        return abort(404)
    list.update_content(item, bool(check))
    db.session.commit()
    return jsonify({'status': 'ok', 'list': list.content[item]})


@app.route('/list/_search/<task>')
def list_task_exist(task):
    list = List.query.filter(
        func.json_search(List.content, 'ONE', task)).all()
    if list is None:
        return abort(404)
    return jsonify({'status': 'ok', 'list': ListSchema(many=True).dump(list)})
