#importing flask for using 
from flask import Flask , request
#importing the DataBase
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
app.app_context().push()


#defining the class Books

class Books_data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    book_name = db.Column(db.String(80), unique = True, nullable = False)
    author = db.Column(db.String(150))
    publisher = db.Column(db.String(200))

    def __repr__(self):
        return f"{self.id} - {self.author} - {self.book_name} - {self.publisher}"

#making the first route or the first for app
@app.route('/')
def index():
    return 'Hello!'

#making the second webpage
@app.route('/Books')
def get_books():
    books = Books_data.query.all()
    output = []
    for book in books:
        book_data = {'id' : book.id, 'author' : book.author,
                     'book_name': book.book_name, 'publisher': book.publisher
                     }
        output.append(book_data)
    return {'Books' : output}

#making the third webpage 
@app.route('/Books/<id>')
def get_id(id):
    book = Books_data.query.get(id)
    return {'id' : book.id, 'author' : book.author,'book_name': book.book_name, 'publisher': book.publisher}



@app.route('/Books', methods= ['POST'])
def add_books():
    book = Books_data (book_name = request.json['book_name'], author = request.json['author'], publisher = request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id' : book.id, 'author' : book.author,'book_name': book.book_name, 'publisher': book.publisher}


#making a function based to delete data by using postman and using the 'DELETE' method

@app.route('/Books/<id>', methods = ['DELETE'])
def delete_book(id):
    book = Books_data.query.get(id)

    if book is None:
        return {'message': ' There is no record...'}
    
    db.session.delete(book)
    db.session.commit()

    return {'message':'Record Deleted!'}









if __name__ == "__main__":
    app.run()