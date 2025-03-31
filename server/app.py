from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

def safe_eval(expression):
    """Securely evaluate math expressions with PEMDAS support"""
    try:
        # Validate characters
        if not re.match(r'^[\d+\-*/().\s]+$', expression):
            return {"error": "Invalid characters"}
        
        # Check balanced parentheses
        if expression.count('(') != expression.count(')'):
            return {"error": "Unbalanced parentheses"}
        
        # Convert to Python expression and evaluate
        result = eval(expression, {'__builtins__': None}, {})
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression', '')
    return jsonify(safe_eval(expression))

if __name__ == '__main__':
    app.run(debug=True, port=5000)