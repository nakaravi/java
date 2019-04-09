from flask import Flask, jsonify, request

app = Flask(__name__)
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            data = request.get_json()
			print(data)
            #years_of_experience = float(data["yearsOfExperience"])
            
            #lin_reg = joblib.load("./linear_regression_model.pkl")
			data = {'result':'success','data':[{'name':'ravi'},{'name':'kumar'}]}
			return jsonify(data)
        except ValueError:
            return jsonify("Please enter a number.")
			
		
        #return jsonify(lin_reg.predict(years_of_experience).tolist())
if __name__ == '__main__':
	app.debug=True
	app.run()
	
