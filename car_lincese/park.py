# https://parkingfee.pma.gov.taipei
# post
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import requests
from IPython.display import Image
from PIL import Image
import pytesseract
import cv2
import numpy as np
import time
import warnings
from urllib3.exceptions import InsecureRequestWarning
import json
from binascii import a2b_base64

headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

def findResult(rs, payload):
	result = []
	warnings.simplefilter('ignore',InsecureRequestWarning)
	r = rs.post('https://parkingfee.pma.gov.taipei/Home/TicketQuery', data = payload, verify = False, headers = headers)
	soup = BeautifulSoup(r.text, 'html.parser')
	if soup is None:
		return (payload['CarID'] + ": \n")
	table = soup.find('table', {'class' : 'responsive_table'})
	if table is None:
		return (payload['CarID'] + ": \n")
	tbody = table.find('tbody')
	if tbody is None:
		return (payload['CarID'] + ": \n")
	rows = tbody.find_all('tr')
	result_str = ""
	for i in rows:
		if i.find_all('td'):
			tds = i.find_all('td')
			if len(tds) > 0:
				result.append({
				"日期":tds[0].text,
				"時間":tds[1].text,
				"停車單號":tds[3].text,
				"應繳金額":tds[4].text.strip(' \t\n\r'),
				"繳費期限":tds[5].text.strip(' \t\n\r'),
				})
				result_str = '\n'.join(str(i) for i in result)
	return (payload['CarID'] + ": \n" + result_str)
    
def getValidateCode(rs):
	warnings.simplefilter('ignore',InsecureRequestWarning)
	r = rs.post('https://parkingfee.pma.gov.taipei/Home/ChangeImageSource', verify = False, stream = True, headers = headers)
	j = json.loads(r.text)
	img_data = j["codeString"][22:]
	binary_data = a2b_base64(img_data)

	f = open('code.png', 'wb')
	f.write(binary_data)
	f.close()

def checkValidateCode():
	img = Image.open('code.png').convert('L')
	ret,img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)
	img = Image.fromarray(img.astype(np.uint8))
	pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
	code = pytesseract.image_to_string(img)

	return code.strip()

if __name__ == '__main__':
	rs = requests.session()
	warnings.simplefilter('ignore',InsecureRequestWarning)
	r = rs.get('https://parkingfee.pma.gov.taipei/', verify = False, headers = headers)
	
	f = open('card_random.txt', 'r')
	lines = f.readlines()
	f.close()

	fw = open('card_query_result.txt', 'w')

	for i in range(len(lines)):
		# 忽略空白
		line = lines[i].strip()
		line = lines[i].split(',')
		line[1] = line[1].strip()

		rs = requests.session()
		getValidateCode(rs)

		payload = {
			'CarID': line[0],
			'CarType': line[1], #機車為M 汽車為C
			'ValiCode': checkValidateCode()
		}

		result = findResult(rs, payload)
		print("next...")
		fw.write(result + "\n")

	fw.close()

