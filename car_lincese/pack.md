1. 安裝 install PyInstaller from PyPI
`pip install pyinstaller`

2. 	-h :help
	-F :將程式打包成單一執行檔(適合較簡易的代碼或只有單一.py檔)
	-D :打包多個文件，exe檔及依賴的東西會一起放置在dist資料夾內(適合框架形式的程式)
`pyinstaller -F park.py`

3. dist/xxxx.exe