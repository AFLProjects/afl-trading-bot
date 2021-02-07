import urllib.request

# Get Price from yahoo website
def IBGetPrice(stock):
	html = ""
	with urllib.request.urlopen(url) as f:
	    html = f.read().decode('utf-8')
	html = getHtml('https://finance.yahoo.com/quote/{}?p={}'.format(stock, stock))
	html = html.split('My(6px) Pos(r) smartphone_Mt(6px)',1)[1];
	html = html.split('<span',1)[1];
	html = html.split('>',1)[1];
	html = html.split('</span>',1)[0];
	html = float(html.replace(',',''))
	return html
