# psdirect-queue
I offer no support or anything related to this script. May have more success if you browse YouTube or something a little bit in the browser that opens initially.

# Installation
From PowerShell:

```
git clone https://github.com/ima9rd/psdirect-queue.git  
cd psdirect-queue  
python -m venv env  
./env/Scripts/activate  
pip install -r requirements.txt  
python app.py
```

If you encounter errors such as `No module named win32com.client, No module named win32, or No module named win32api`, you will need to install `pypiwin32`:
```
pip install pypiwin32
```