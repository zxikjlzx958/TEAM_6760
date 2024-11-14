# TEAM_6760

## Preprocess資料夾
包含用於資料前處理之程式碼 data_preprocess.py
請參考Preprocess/README.md

## Model資料夾
包含用於資料檢索之程式碼 retrieval.py
請參考Model/README.md

## main.py
用於執行data_preprocess.py和retrieval.py之程式碼    
需要將資料集放至程式碼指定之路徑或根據資料集路徑修改程式碼  
> 或者單獨執行data_preprocess.py和retrieval.py

## Usage
```
python main.py
```

## Environment
python版本為3.10.15  
安裝必要套件可執行  
```
pip install -r requirements.txt
```
前處理部份需要額外安裝與設定tesseract及其chi_tra language pack  
詳細環境資訊請參考env.txt  

## 大型模型
所使用之大型模型：[BAAI/bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3)
使用方式如retrieval.py之程式碼
