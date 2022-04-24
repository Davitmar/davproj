from app import create_app
from app.db import db
from scraping import get_universities
from app.universities.models import University
from app.countries.models import Country

if __name__ == '__main__':
    app = create_app()
    app.app_context().push()
    db.create_all()

    universities = get_universities()

    countries = {}  # {'USA':1, 'FRANCE':2}
    for u in universities:
        name = u['country']
        if name not in countries:
            c = Country(name=name)
            db.session.add(c)
            db.session.flush()
            db.session.refresh(c)
            countries[name] = c.id

            # last_added = Country.query.filter_by(name=name).first()
            # country_id = last_added.id

    for u in universities:
        country_name = u['country'] # USA
        university = University(
            rank=u['rank'],
            name=u['name'],
            country_id=countries[country_name],
            score=u['score']
        )
        db.session.add(university)
    db.session.commit()
