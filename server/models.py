from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here
class Research(db.Model, SerializerMixin):
    __tablename__ = 'research'

    serialize_rules = ('-authors.research',)

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    research_authors = db.relationship('ResearchAuthors', back_populates='research')
    authors = association_proxy('research_authors', 'authors')

    @validates('research')
    def validate_research(self, key, year):
        if len(year) != 4:
            raise ValueError("Year must be 4 digits")
        return year


class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'

    serialize_rules = ('-research.authors',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    research_authors = db.relationship('ResearchAuthors', back_populates='author')
    research = association_proxy('research_authors', 'research')

    @validates('field_of_study')
    def  validate_field_of_study(self, key, field):
        field_list = ["AI", "Robotics", "Machine Learning", "Vision", "Cybersecurity"]
        if field != field_list:
            raise ValueError("Invalid field of study")
        return field

class ResearchAuthors(db.Model, SerializerMixin):
    __tablename__ = 'research_authors'

    serialize_rules = ('-author.research_authors', '-research.research_authors',)

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    research_id = db.Column(db.Integer, db.ForeignKey('research.id'))

    author = db.relationship('Author', back_populates='research_authors')
    research = db.relationship('Research', back_populates='research_authors')