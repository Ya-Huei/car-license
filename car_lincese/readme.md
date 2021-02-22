此軟體只支援Windows（64位元）之作業系統，請知悉。
1. 執行tesseract-ocr-w64-setup.exe安裝在"C:/Program Files/Tesseract-OCR"。
2. 安裝結束後確認在"C:/Program Files/Tesseract-OCR"是否有"tesseract.exe"檔案。若無則代表您裝錯了，請重新安裝。
3. 將車牌資訊輸入於"card_random.txt"文件內，輸入格式為：
	XXX-XXXX,[Type]
	- Type：M表示為機車、C表示為汽車
4. 執行park.exe並且等待。
5. 結果將輸出於"card_query_result.txt"。