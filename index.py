from flask import Flask, render_template

app = Flask(__name__)

# Rota para a página inicial


@app.route('/')
def home():
    # Passa parâmetros para o template
    # 'css' e 'js' são opcionais
    page = {
        'title': 'Biscoito',
        'css': 'home.css',
        'js': 'home.js'
    }

    return render_template('home.html', page=page)


@app.route('/contacts')
def contacts():

    page = {
        'title': 'Contatos',
        'css': 'home.css',
        'js': 'contacts.js'
    }

    return render_template('contacts.html', page = page)

@app.route('/about')
def about():
    
    page = {
        'title': 'Sobre',
        'css': 'home.css',
        'js': 'about.js'
    }
    
    return render_template('about.html', page = page)

if __name__ == '__main__':
    app.run(debug=True)
