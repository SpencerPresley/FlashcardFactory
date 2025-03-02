from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/flashcards/<filename>')
def get_flashcards(filename):
    return render_template('index.html', filename=filename)

@app.route('/<filename>')
def index(filename):
    print(filename)
    return render_template('index.html', filename=filename)

@app.route('/public/<path:filename>')
def serve_static(filename):
    return send_from_directory('public', filename)

@app.route('/styles/<path:filename>')
def serve_styles(filename):
    return send_from_directory('styles', filename)


if __name__ == '__main__':
    app.run(debug=True)