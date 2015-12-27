from flask import Flask, render_template, request, redirect, flash
import mains.mp_infos as mp

app = Flask(__name__)
app.config['SECRET_KEY'] = '6r93dcjdJZ8s56468tA9c5CZZ31mVet2'

@app.route('/')
@app.route('/index.html')
def index():
    # return 'Hello World!'
    json_res = mp.mp_info(10162)
    return render_template('index.html', json_res=json_res)


@app.route('/filter.html', methods=['POST', 'GET'])
def filtering():
    policies = mp.get_policies()

    if request.method == 'POST':
        policy = request.form['policy']
        print(str(policy))

        vote = request.form['vote']
        print(str(vote))


    return render_template('filter.html', policies=policies)


if __name__ == '__main__':
    app.run(debug=True)




    # json_res = mp_info(10162)
    # return render_template('index.html',json_res)
