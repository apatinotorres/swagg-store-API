import requests
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)
model = []


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/new_pet', methods=['GET'])
def person():
    return render_template('new_pet.html')


@app.route('/pet_detail', methods=['POST'])
def pet_detail():
    api_url = "https://petstore.swagger.io/v2/pet"
    id = request.form['id']
    name = request.form['name']
    new_data = {
                    "id": id,
                    "category": {
                        "id": 0,
                        "name": "string"
                    },
                    "name": name,
                    "photoUrls": [
                        "string"
                    ],
                    "tags": [
                        {
                            "id": 0,
                            "name": "string"
                        }
                    ],
                    "status": "available"
                }
    response = requests.post(api_url, json=new_data)
    return render_template('pet_detail.html', value=(id, name))


@app.route('/pet', methods=['GET'])
def pets(status: str = "pending"):
    url2 = "https://petstore.swagger.io/v2/pet/findByStatus?status={0}".format(status)
    response = requests.get(url2)
    data_pets = [(i['id'], i['name'], i['status']) for i in response.json()]
    return render_template('pets.html', value=data_pets)


@app.route('/pet_update/<id_pet>', methods=['GET'])
def pet_update(id_pet):
    return render_template('pet_update.html', value=id_pet)


@app.route('/pet_update_detail', methods=['POST'])
def pet_update_detail():
    api_url_update = "https://petstore.swagger.io/v2/pet"
    id = request.form['id']
    name = request.form['name']
    status = request.form['status']
    update_data = {
                        "id": id,
                        "category": {
                            "id": 0,
                            "name": "string"
                        },
                        "name": name,
                        "photoUrls": [
                            "string"
                        ],
                        "tags": [
                            {
                                "id": 0,
                                "name": "string"
                            }
                        ],
                        "status": status
                    }
    response = requests.put(api_url_update, json=update_data)
    return render_template('pet_detail.html', value=(id, name, status))


@app.route('/pet_delete/<id_pet>', methods=['GET'])
def pet_delete(id_pet):
    api_url = "https://petstore.swagger.io/v2/pet/{0}".format(id_pet)
    response = requests.delete(api_url)
    return render_template('pet_detail.html', value="Delete successfully")

### Store


@app.route('/store', methods=['GET'])
def show_store():
    return render_template("store.html")

@app.route('/store/inventory')
def show_inventory():
    url = "https://petstore.swagger.io/v2/store/inventory"
    response = requests.get(url)
    data = [( i, response.json()[i] ) for i in response.json()]
    # print(data)
    return render_template('inventory.html', value = data)

@app.route('/place_order/<id_pet>', methods=['GET'])
def place_order(id_pet):
    api_url_order = "https://petstore.swagger.io/v2/store/order"
    randomnumber = random.randint(1, 10)
    orders = {
        "id": randomnumber,
        "petId": id_pet,
        "quantity": 1,
        "shipDate": "2023-04-02T15:40:56.635Z",
        "status": "placed",
        "complete": "true"
    }
    response = requests.post(api_url_order, json=orders)
    return render_template('place_order.html', value=orders)

@app.route('/store/find_order')
def find_order():
    order_id = request.form['id']
    api_url_find_order = "https://petstore.swagger.io/v2/store/order/{0}".format(order_id)
    response = requests.get(api_url_find_order)
    order_found = response.json()
    return render_template('find_order.html', value=order_found)

@app.route('/order_delete', methods=["POST"])
def order_delete():
    order_id = request.form['id']
    delete_url = "https://petstore.swagger.io/v2/store/order/{0}".format(order_id)
    response = requests.delete(delete_url)
    return render_template('order_delete.html')





### User

@app.route('/create_user', methods=['POST'])
def create_user():
    url = 'https://petstore.swagger.io/v2/user'
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    id = random.randint(1, 1000)
    model_user = {
        "id": id,
        "username": username,
        "firstName": "mori",
        "lastName": "mori",
        "email": email,
        "password": password,
        "phone": "3243",
        "userStatus": 0
    }
    response = requests.post(url, json=model_user)
    return render_template('create_user.html', value=model_user)


@app.route('/user', methods=['GET'])
def user():
    return render_template('user.html')


@app.route('/user_log', methods=['GET', 'POST'])
def user_log():
    username = request.form['username']
    password = request.form['password']
    url = 'https://petstore.swagger.io/v2/user/login?username={0}&password={1}'.format(username, password)
    response = requests.get(url)
    user_info = response.json()
    return render_template('user_log.html', value = user_info)


@app.route('/log_out', methods=['GET'])
def log_out():
    url = 'https://petstore.swagger.io/v2/user/logout'
    response = requests.get(url)
    return render_template('log_out.html', value='Salida exitosa')

'''
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
'''
if __name__ == '__main__':
    app.run()
