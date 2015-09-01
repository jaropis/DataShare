from . import db
## many to many association table between keyword  and dataset
association_table = db.Table('association', db.Model.metadata,
                          db.Column('dataset_id', db.Integer, db.ForeignKey('dataset.id')),
                          db.Column('keyword_id', db.Integer, db.ForeignKey('keyword.id'))
                          )
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    fullname = db.Column(db.String(80))
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s', email='%s')>" % (
            self.name, self.fullname, self.password, self.email
            )

class DataSet(db.Model):
    __tablename__='dataset'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    numberOfFiles = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='dataset')
    ## many-to-many with KeyWord
    keywords = db.relationship('KeyWord', secondary=association_table, backref = 'dataset')
    ## one-to-many with Category (is one)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref = 'dataset')
    def __repr__(self):
        return "<Dataset(name='%s', numberOfFiles='%s', user='%s', category='%s')>" % (
            self.name, self.numberOfFiles, self.user.name, self.category
            )

class KeyWord(db.Model):
    __tablename__ = 'keyword'
    
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    keyword = db.Column(db.String(80), nullable=False)

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    category_name = db.Column(db.String(80), nullable = False)
