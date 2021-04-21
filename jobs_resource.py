from flask.json import jsonify
from flask_restful import Resource, abort
from werkzeug.security import generate_password_hash

from data import db_session
from data.jobs import Jobs
from parsers import job_parser as parser


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    print(job)
    if not job:
        abort(404, message=f"job {job_id} not found")


class jobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict()})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class jobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        job = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict() for item in job]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            team_leader=args['team_leader'],
            description=args['description'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            start_date=args['start_date'],
            end_date=args['end_date'],
            is_finished=bool(args['is_finished'])
        )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})
