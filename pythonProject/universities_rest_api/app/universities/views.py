from app.countries.models import Country
from app.db import db
from app.universities.models import University
from flask import Blueprint, jsonify, request
from flask.views import MethodView

bp = Blueprint('university', __name__)


class UniversitiesBaseView(MethodView):
    def data_validation(self, data):
        errors = {}
        field = {
            'name': str,
            'score': float,
            'rank': int,
            'country_id': int
        }

        for name, _type in field.items():
            try:
                _type(data[name])
            except (ValueError, TypeError, KeyError):
                errors[name] = 'invalid'

        return data, errors

    def is_column_is_unique(self, col, val):
        return University.query.filter_by(**{col: val}).first()

    def get_country_by_id(self, country_id):
        return Country.query.get(country_id)


class UniversitiesListCreateView(UniversitiesBaseView):

    def get(self):
        limit = 20
        rows = University.query

        country = int(request.args.get('country'))

        if country:
            rows = rows.filter_by(country_id=country)

        rows = rows.limit(limit)

        page = request.args.get('page', '1')
        if page and page.isnumeric():
            page = int(page)
            offset = (page - 1) * limit
            rows = rows.offset(offset)

        response = [{
            'id': row.id,
            'rank': row.rank,
            'name': row.name,
            'country_id': row.country_id,
            'score': row.score
        } for row in rows]

        return jsonify(response)

    def post(self):
        data = request.json
        data, errors = self.data_validation(data)

        if len(errors):
            return jsonify(errors), 401

        if not self.get_country_by_id(data['country_id']):
            errors['country'] = 'invalid'

        if self.is_column_is_unique('name', data['name']):
            errors['name'] = 'invalid'

        if self.is_column_is_unique('rank', data['rank']):
            errors['rank'] = 'invalid'

        if len(errors):
            return jsonify(errors), 401

        u = University(**data)
        db.session.add(u)
        db.session.commit()
        db.session.refresh(u)
        return jsonify({'id': u.id}), 201


class UniversitiesDetailsUptadeDeleteView(UniversitiesBaseView):
    def get(self, u_id):
        # if there is no university return jsonify({}), 404

        rows = University.query

        if u_id and u_id.isnumeric():
            u_id = int(u_id)
            if not rows.filter_by(id=u_id).first():
                return jsonify({}), 404

            row=rows.filter_by(id=u_id).first()

        response = {
            'id': row.id,
            'rank': row.rank,
            'name': row.name,
            'country_id': row.country_id,
            'score': row.score
        }

        return jsonify(response)

    def put(self, u_id):
        # if there is no university return jsonify({}), 404
        data = request.json
        data, errors = self.data_validation(data)

        if len(errors):
            return jsonify(errors), 401

        if not self.get_country_by_id(data['country_id']):
            errors['country'] = 'invalid'

        if self.is_column_is_unique('name', data['name']) and self.is_column_is_unique('name', data['name']).id != int(u_id):
            errors['name'] = 'invalid'
        # #
        if self.is_column_is_unique('rank', data['rank']) and self.is_column_is_unique('rank', data['rank']).id != int(u_id):
            errors['rank'] = 'invalid'

        if len(errors):
            return jsonify(errors), 401

        rows=University.query

        if u_id and u_id.isnumeric():
            u_id = int(u_id)
            if not rows.filter_by(id=u_id).first():
                return jsonify({}), 404
            upd_row=rows.filter_by(id=u_id).first()
            upd_row.rank=data['rank']
            upd_row.name = data['name']
            upd_row.country_id = data['country_id']
            upd_row.score = data['score']
            db.session.commit()


            return jsonify({'id': u_id}), 201
    #
    def delete(self, u_id):
        # if there is no university return jsonify({}), 404
        rows = University.query

        if u_id and u_id.isnumeric():
            u_id = int(u_id)
            if not rows.filter_by(id=u_id).first():
                return jsonify({}), 404

        rows.filter_by(id=u_id).delete()
        db.session.commit()

        return jsonify({'deleted': u_id})


bp.add_url_rule('/universities/', view_func=UniversitiesListCreateView.as_view('universities'))
bp.add_url_rule('/universities/<u_id>/', view_func=UniversitiesDetailsUptadeDeleteView.as_view('university'))
