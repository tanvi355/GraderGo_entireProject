from flask import Flask,jsonify,request
import util



app = Flask(__name__)

@app.route('/')
def hello():
    return 'GraderGo API'

@app.route('/predict',methods=['GET','POST'])
def predict():

    if request.method=='POST':
        essay=(request.form.get('essay'))
        print(essay)

        data=util.preprocess(essay)
        score=util.predict(data)
        score=str(score[0])
        print(score,type(score))

        score=jsonify(
            {
                'pred_score': score
            }
        )
        score.headers.add('Access-Control-Allow-Origin', '*') #Allows cross origin

        return score
    else:
        return 'Send the request using post method'



if __name__=='__main__':
    util.loading_artifacts()
    app.run(port=51,debug=True)