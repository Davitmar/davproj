# from app.countries.models import Country
# from app.db import db
# from app.universities.models import University
# from flask import Blueprint, jsonify, request
# from flask.views import MethodView
#
# bp = Blueprint('university', __name__)
#
#
# class UniversitiesBaseView(MethodView):
#     def data_validation(self, data):
#         errors = {}
#         field = {
#             'name': str,
#             'score': float,
#             'rank': int,
#             'country_id': int
#         }
#
#         for name, _type in field.items():
#             try:
#                 _type(data[name])
#             except (ValueError, TypeError, KeyError):
#                 errors[name] = 'invalid'
#
#         return data, errors
#
#     def is_column_is_unique(self, col, val):
#         return University.query.filter_by(**{col: val}).first()
#
#     def get_country_by_id(self, country_id):
#         return Country.query.get(country_id)
#
#
#
# class UniversitiesDetailsUptadeDeleteView(UniversitiesBaseView):
#     def get(self, u_id):
#         # if there is no university return jsonify({}), 404
#         return jsonify({'id': 'u.id'})
#         # rows = University.query
#         #
#         # if u_id and u_id.isnumeric():
#         #     u_id = int(u_id)
#         #     row=rows.filter_by(id=u_id).first()
#         #
#         # response = {
#         #     'id': row.id,
#         #     'rank': row.rank,
#         #     'name': row.name,
#         #     'country_id': row.country_id,
#         #     'score': row.score
#         # }
#
#         #return jsonify(response)
#
#     def put(self, u_id):
#         # if there is no university return jsonify({}), 404
#         return jsonify({'id': 'u.id'})
#
#     def delete(self, u_id):
#         # if there is no university return jsonify({}), 404
#         pass
#
#
# bp.add_url_rule('/universities/', view_func=UniversitiesListCreateView.as_view('universities'))
# bp.add_url_rule('/universities/<u_id>/', view_func=UniversitiesDetailsUptadeDeleteView.as_view('university'))
