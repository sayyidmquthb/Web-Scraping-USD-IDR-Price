from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

table = soup.find('table', attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
tr = table.find_all('tr')

currency = [] #initiating a tuple

for i in range(1, len(tr)):
    row = table.find_all('tr')[i]

    if len(row)!=1:
        #get date
        date = row.find_all('td')[0].text
        date = date.strip()

        #get price
        price = row.find_all('td')[2].text
        price = price.strip()
    currency.append((date,price))
    
currency

#change into dataframe
data = pd.DataFrame(currency, columns = ('Date','Price USD/IDR'))
data = data[::-1]

#insert data wrangling here
data['Date'] = pd.to_datetime(data['Date'])
data['Price USD/IDR'] = data['Price USD/IDR'].str.replace(',', '')
data['Price USD/IDR'] = data['Price USD/IDR'].str.replace(' IDR', '')
data['Price USD/IDR'] = data['Price USD/IDR'].astype('float64')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {data["Price USD/IDR"].mean().round(2)}'

	# generate plot
	ax = data.plot(figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
