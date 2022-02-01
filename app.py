'''
Date: 2021-11-04 13:47:40
LastEditors: GC
LastEditTime: 2021-11-07 20:48:26
FilePath: \Flask-Blog-Project\app.py
'''
from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
