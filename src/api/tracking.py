import urllib.request

def getStockPrice(stock):
	html = ""
	with urllib.request.urlopen('https://finance.yahoo.com/quote/{}?p={}'.format(stock, stock)) as f:
	    html = f.read().decode('utf-8')
	html = html.split('My(6px) Pos(r) smartphone_Mt(6px)',1)[1];
	html = html.split('<span',1)[1];
	html = html.split('>',1)[1];
	html = html.split('</span>',1)[0];
	html = float(html.replace(',',''))
	return html
