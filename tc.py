from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Import text for raw SQL execution

app = Flask(__name__)

# Configure the database URI: replace 'username' and 'password' with your database credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/coderr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Route to test the database connection
@app.route('/test_db_connection')
def test_db_connection():
    try:
        # Execute a simple query to test the connection
        db.session.execute(text('SELECT 1'))
        return 'Database connection successful!'
    except Exception as e:
        return f'Database connection failed: {e}'
@app.route('/contact', methods=['POST'])
def add_contact():
    data = request.json
    new_contact = Contact(
        name=data.get('name'),
        email=data.get('email'),
        phone_num=data.get('phone_num'),
        message=data.get('message')
    )
    db.session.add(new_contact)
    db.session.commit()
    #return jsonify({'message': 'Contact added successfully!'})
    return render_template("contact.html")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
