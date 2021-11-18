from flask import Flask, request
from flask_restful import Resource, Api, abort
import sqlite3

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, World!'}

class Movies(Resource):

    db_path = 'movies.sqlite3'

    database_columns = {
        'title' : str,
        'release_date' : str,
        'genre' : str,
        'mpaa_rating' : str,
        'total_gross' : int,
        'inflation_adjusted_gross' : int
    }

    ### Helper Functions ###

    def get_db_cursor(self):
        return sqlite3.connect(self.db_path).cursor()

    def label_tuples(self, tuples):
        return [dict(zip(self.database_columns, t)) for t in tuples]

    def abort_on_exception(self, error : str):
        '''Abort with 500 Interal Server Error'''
        return abort(500, message=f'An unknown error occurred: {error}', )

    def abort_on_does_not_exist(self, title : str):
        '''Abort with 404 and a message when title cannot be found'''
        return abort(404, f'Move of title "{title}" does not exist')

    def abort_if_does_not_exist(self, title : str):
        '''Abort a request if a movie with title cannot be found'''
        cur = self.get_db_cursor().execute('SELECT * FROM movies WHERE title=?', [title])
        exists = bool(cur.fetchone())
        if not exists:
            self.abort_on_does_not_exist(title)

    ### API Endpoints ###

    def get(self, title):
        '''HTTP GET requests'''
        self.abort_if_does_not_exist(title)
        cur = self.get_db_cursor()
        try:
            cur.execute('SELECT * FROM movies WHERE title=:title', {'title' : title})
        except sqlite3.Error:
            return self.abort_on_exception()
        objs = self.label_tuples(cur.fetchall())
        return objs[0]

    def put(self, title):
        '''HTTP PUT requests'''
        self.abort_if_does_not_exist(title)
        # Input Santization
        cleanForm = {}
        currObj = self.get(title)
        for col in self.database_columns.keys():
            if col not in request.form:
                cleanForm[col] = currObj[col] # Use previous values
            else:
                cleanForm[col] = request.form[col]
        cleanForm['title'] = title
        # Query the database
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        try:
            cur.execute(
                '''
                UPDATE movies
                SET release_date=:release_date,
                    genre=:genre,
                    mpaa_rating=:mpaa_rating,
                    total_gross=:total_gross,
                    inflation_adjusted_gross=:inflation_adjusted_gross
                WHERE title=:title
                ''',
                cleanForm
            )
        except sqlite3.Error as e:
            return self.abort_on_exception(str(e))
        conn.commit()
        # Return the updated entry w/ 200 OK
        return self.get(title)

api.add_resource(HelloWorld, '/hello')
api.add_resource(Movies, '/movies/<string:title>')

if __name__ == '__main__':
    app.run(debug=True)