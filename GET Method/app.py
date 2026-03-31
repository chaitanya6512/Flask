from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/square', methods=['GET'])
def squarenumber():
    num = request.args.get('num')

    if num is None:  # No number entered, show input form
        return render_template('squarenum.html')
    elif num.strip() == '':  # Empty input
        return "<h1>Invalid number. Please enter a number.</h1>"
    try:
        square = int(num) ** 2
        return render_template('answer.html', squareofnum=square, num=num)
    except ValueError:
        return "<h1>Invalid input. Please enter a valid number.</h1>"

if __name__ == '__main__':
    app.run(debug=True)



# Explanation:
# request.args.get('num') retrives the number from the URL paramters.
# if num is None, the user is visiting the page for the first time otherwise an error message is displayed.
# the square of the number is calculated and passed to the answer.html template.