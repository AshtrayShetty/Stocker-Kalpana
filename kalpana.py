from flask import Flask, render_template, redirect, request, url_for
from prophet import pred

app=Flask(__name__)

#Home Page
@app.route('/')
@app.route('/stock')
def home():
    return render_template('home.html')

#Page For Form.
#Accepts Values For Company Name And Time (In Years)
#Time In Years Accepted From 1 To 5 Only (Because The Table Gets Very Large) 
@app.route('/predict', methods=['GET','POST'])
def form():
	return render_template('form.html')

#Page To Display The Predicitons For The Accepted Form Parameters
#Displays The Prediction Table For Each Day From "5-5-2018" To "5-5-{2018+the_time_specified_in_form}"
@app.route('/prediction', methods=['GET','POST'])
def display(*args,**kwargs):

	if request.method=='GET':
		cmp1=request.args['company']
		time=request.args['time']

		#Validation Check (So That People Enter The Time Period Only Between 1 To 5 Years)
		if time in [str(num) for num in range(1,6)]:

			try:
				#Object For Prediction Created. Stores The Values Of Company And Time Obtained From The Form
				context=pred(cmp1, time)
				#Gets The Predicted Dataframe As A String (HTML) Object 
				dataframe=context.predictor()[0]
				#Gets The Plot Of Predciction Versus Time (Over The Intervals Of 1 Year)
				url_figure=context.predictor()[1]
				#Gets The Plot For Weekly Changes, Monthly Changes And Changes In Trend Over Regular Intervals
				url_figure3=context.predictor()[2]
				return render_template('display.html', context=context, dataframe=dataframe, url_figure=url_figure, url_figure3=url_figure3)

			except:
				return render_template('404.html')

		return render_template('404.html')

	return redirect(url_for('home'))	

if __name__=='__main__':
	app.run(debug=True) 