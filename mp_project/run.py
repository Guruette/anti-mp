from flask import Flask, render_template, request, redirect, flash
import mains.mp_infos as mp

app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def index():
    # return 'Hello World!'
    json_res = mp.mp_info(10162)
    return render_template('index.html', json_res=json_res)


@app.route('/filter.html', methods=['POST', 'GET'])
def filtering():
    policies = mp.get_policies()

    # drop_down_value = request.form['drop_down']
    # print("value  ",drop_down_value)

    return render_template('filter.html', policies=policies)


if __name__ == '__main__':
    app.run(debug=True)




    # json_res = mp_info(10162)
    # return render_template('index.html',json_res)
