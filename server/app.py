#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Research, Author, ResearchAuthors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api= Api(app)

# Research -  get()
class Researchs(Resource):
    def get(self):
        research_papers = [research.to_dict() for research in Research.query.all()]
        return research_papers, 200

# ResearchById - get(), delete()
class ResearchById(Resource):
    def get(self, id):
        try:
            research_paper = Research.query.filter_by(id=id).first()
            return research_paper.to_dict(), 200
        except:
            return {'error': 'Research paper not found'}, 404

    def delete(self, id):
        try:
            research_paper = Research.query.filter_by(id=id).first()
            db.session.delete(research_paper)
            db.session.commit()
            return '', 200
        except:
            return {'error': 'Research paper not found'}, 404


# Authors - get()
class Authors(Resource):
    def get(self):
        authors = [author.to_dict() for author in Author.query.all()]
        return authors, 200

#ResearchAuthors - post()
class ResearchAuthor(Resource):
    def post(self):
        try:
            new_research = ResearchAuthors(
                author_id=request.form['author_id'],
                research_id=request.form['research_id'],
            )
            db.session.add(new_research)
            db.session.commit()
            return new_research.to_dict(), 201
        except:
            return {'error': 'Unable to create new research'}, 400


api.add_resource(Researchs, '/research')
api.add_resource(ResearchById, '/research/<int:id>')
api.add_resource(Authors, '/authors')
api.add_resource(ResearchAuthor, '/researchauthors')



if __name__ == '__main__':
    app.run(port=5555, debug=True)
