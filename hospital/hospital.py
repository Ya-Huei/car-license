# https://webreg.tpech.gov.tw/RegOnline3_1.aspx?ChaId=A103&tab=3
# post
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import requests
import shutil
from IPython.display import Image
from PIL import Image
import pytesseract
import cv2
import numpy as np
import certifi
import warnings
from urllib3.exceptions import InsecureRequestWarning

headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

def findResult(payload):
	result = []
	warnings.simplefilter('ignore',InsecureRequestWarning)
	r = requests.post('https://webreg.tpech.gov.tw/RegOnline3_1.aspx?ChaId=A103&tab=3', data = payload, verify = False, headers = headers)
	soup = BeautifulSoup(r.text, 'html.parser')
	if soup is None:
		return ''
	div = soup.find('div', {'id' : 'print_body'})
	if div is None:
		return ''
	table = div.find('table')
	if table is None:
		return ''
	rows = [[ele.text.strip() for ele in item.find_all("td")]
		for item in table.find_all("tr")]

	result_str = ""
	for data in rows:
		result.append(data)

	result_str = '\n'.join(str(i) for i in result)
	return result_str
    
def getValidateCode(rs):
	r = rs.post('https://webreg.tpech.gov.tw/ValidateCode.aspx', stream = True, headers = headers)
	f = open('code.png', 'wb')
	shutil.copyfileobj(r.raw, f)
	f.close()

def checkValidateCode():
	img = Image.open('code.png').convert('L')
	ret,img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)
	img = Image.fromarray(img.astype(np.uint8))
	code = pytesseract.image_to_string(img)
	return code

if __name__ == '__main__':
	f = open('hospital.txt', 'r')
	lines = f.readlines()
	f.close()

	fw = open('hospital_result.txt', 'w')

	for i in range(len(lines)):
		# 忽略空白
		line = lines[i].strip()
		line = lines[i].split(',')

		rs = requests.session()
		getValidateCode(rs)

		payload = {
			'no': line[0].strip(),
			'y1': line[1].strip(),
			'm1': line[2].strip(),
			'd1': line[3].strip(),
			'YRadio': 'on',
			'Button1': '查詢掛號',
			'TextBox1' : checkValidateCode()
		}

		result = findResult(payload)
		# fw = open('cardQuery_result.txt', 'w')
		# print(result);
		# fw.write(result)
		# fw.close()
		# result = findResult(rs, payload)
		fw.write(line[0].strip() + ":\n " + result + "\n\n")

	fw.close()

