import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import seaborn as sns
from fbprophet import Prophet

class pred:

	#Constructor To Accept Values Company Name And Time Values From The Form
	def __init__(self, cmp1, time):
		self.cmp1=cmp1
		self.time=time

	#Machine Learning Which Predicts The Future Stock Prices
	def predictor(self):
		stock=pd.read_csv('BSE_30.csv')

		#Obtaining The Dataframe Values For The Company Specified In The Form
		a=stock.loc[stock['Symbol']==self.cmp1]
		#Obtaining Only Those Values From The Datframe Which Are Necessary For The Predictions
		a=a[['Date', 'Close']] 
		#Renaming The Columns So That It's Understandable By The Learning Model
		a=a.rename(columns={'Date':'ds', 'Close':'y'})

		#Applying The Learning Model Algorithm Over The Dataframe
		m=Prophet()
		m=m.fit(a)

		#Making The Prediction Table For The Time Specified
		future=m.make_future_dataframe(periods=int(self.time)*365)

		#Obtaining The Prediction Table Values For The Time Specified To Display On The Web Page
		df=m.predict(future).tail(int(self.time)*365)

		#Renaming The Columns Of The Prediction Dataframe So That It's Understandable By The User
		columns_renamed={
			'ds':'Date',
			'yhat_lower':'Prediction Lower Bound',
			'yhat_upper':'Prediction Upper Bound',
			'weekly_lower':'Weekly Lower Bound',
			'weekly_upper':'Weekly Upper Bound',
			'yearly_lower':'Yearly Lower Bound',
			'yearly_upper':'Yearly Upper Bound',
		}

		#Taking Only Those Columns Which Are To Be Displayed On The Web Page
		columns_for_prediction=[
			'Date',
			'Prediction Lower Bound',
			'Prediction Upper Bound',
			'Weekly Lower Bound',
			'Weekly Upper Bound',
			'Yearly Lower Bound',
			'Yearly Upper Bound',
		]

		#Obtaining Plot For Stock Price Versus Date (Shows The Stock Prices Change Over The Intervals Of 1 Year)
		figure = m.plot(df, xlabel='Date', ylabel='Price')
		#Address Of Where To Save The Graph
		url_figure=f".\\static\\assets\\img\\graphs\\figure\\{self.cmp1}_{self.time}.png"
		plt.savefig(url_figure)

		#Obtaining Plots For Weekly Changes, Yearly Changes And Trend Changes (In Intervals Of 1 Year)
		figure3 = m.plot_components(df)
		url_figure3=f".\\static\\assets\\img\\graphs\\figure3\\{self.cmp1}_{self.time}.png"
		plt.savefig(url_figure3)

		#Renaming The Columns Of The Prediction Dataframe
		df=df.rename(columns=columns_renamed)

		#Converting The Dataframe To An HTML Table (Stored As A String Object)
		#index=False Removes The Row Values Of The Datarframe
		df=df.to_html(columns=columns_for_prediction, index=False, border=2)

		return [df, url_figure, url_figure3]