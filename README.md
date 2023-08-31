# !dice

### What?
!dice is  a little school project made using flask.

### How to install
It is recommended to use a virtualenv or similar
1. install dependencies `pip install -r requirements`
2. run your favorite WSGI server
    - for development you can use `flask -A dice run --debug`
    - for production [gunicorn](https://gunicorn.org/) is recommended
3. Run the setup at [`http://localhost:5000/admin/setup`](http://127.0.0.1:5000/admin/setup)

### [License](LICENSE)
!dice is licensed under the MIT License
