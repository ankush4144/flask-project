from src.database import Database
from flask import Flask, request
from flask_restplus import Resource, Api, fields

app = Flask(__name__)
api = Api(app)
db_obj = Database()

post_user_credentials = api.model('User', {
     'username': fields.String(required=True,description='Username'),
     'password': fields.String(required=True, min_length=5, description='Password for the username'),
     'firstname': fields.String(required=True,description='first name of the user.'),
     'lastname': fields.String(required=True,description='last name of the user.')
    })


@api.route('/users')
class register_users(Resource):
    def get(self):
        return db_obj.fetch_all_users()
    
    @api.expect(post_user_credentials)
    def post(self):
        #return request.json
        username = request.json['username']
        user_password = request.json['password']
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        try:
            db_obj.insert_users_credentials(username, user_password)
            db_obj.insert_users_information(username, firstname, lastname)
            print(request.json)
            return "Successfully registered user : {}".format(username)
        except Exception as e:
            return "Failed to register user : {} due to following error: \n{}".format(username, e)

@api.route('/users/<string:username>')
class fetch_user_details(Resource):
    def get(self, username):
        return db_obj.fetch_user_details(username)


if __name__ == '__main__':
    app.run(debug=True)
