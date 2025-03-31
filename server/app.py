from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
# Allow requests specifically from your frontend domain
CORS(app, resources={
    r"/calculate": {
        "origins": ["https://binary-calculator-app-1.onrender.com"],
        "methods": ["POST"],
        "allow_headers": ["Content-Type"]
    }
})

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

# Add this to ensure Render compatibility
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Render requires host 0.0.0.0
