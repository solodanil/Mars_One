import flask
from flask import make_response, app, request

from data.jobs import Jobs
from data import db_session

blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_news():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    print(jobs)
    if not jobs:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'jobs': [item.to_dict() for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>')
def get_job(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == job_id).all()
    print(jobs)
    if not jobs:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'jobs': [item.to_dict() for item in jobs]
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'description', 'collaborators', 'is_finished']):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    print(db_sess.query(Jobs).filter(Jobs.id == request.json['id']).first())
    if db_sess.query(Jobs).filter(Jobs.id == request.json['id']).first():
        return make_response(flask.jsonify({'error': 'id already exist'}))
    news = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        description=request.json['description'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'])
    db_sess.add(news)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).get(news_id)
    print(news)
    if not news:
        return flask.jsonify({'error': 'Not found'})
    db_sess.delete(news)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:news_id>', methods=['POST'])
def edit_job(news_id):
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(news_id)
    print(job)
    if not job:
        return flask.jsonify({'error': 'Not found'})
    job.team_leader = request.json.get('team_leader')
    job.description = request.json.get('description')
    job.collaborators = request.json.get('collaborators')
    job.is_finished = request.json.get('is_finished')
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})
