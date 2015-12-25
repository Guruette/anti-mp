from flask import Flask, render_template
import mains.mp_infos as mp

app = Flask(__name__)


@app.route('/')
def index():
    # return 'Hello World!'
    json_res = mp.mp_info(10162)
    return render_template('index.html', json_res=json_res)


if __name__ == '__main__':
    app.run(debug=True)




    # json_res = mp_info(10162)
    # return render_template('index.html',json_res)
