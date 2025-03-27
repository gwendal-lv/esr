import random

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    # Code inutile...
    a = -12
    b = a + 13
    # On choisit un type de chat (au hasard)
    cat_type = random.choice(['black', 'ginger', 'kitten'])
    return render_template('index.html', cat_type=cat_type)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
