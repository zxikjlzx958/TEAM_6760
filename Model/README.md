# Model資料夾
包含用於資料檢索之程式碼 retrieval.py

## retrieval.py
用於進行資料檢索  
讀取question file中所有queries後  
讀取query指定的source txt files  
將文字切分為固定長度（512個字）後   
使用BAAI/bge-reranker-v2-m3模型對每段文字進行reranker  
選取分數最高的文字所屬之文件作為答案  
最後將所有結果以json形式儲存至output_path  
source_path應為前處理的output_path  

### Usage
```
python Model/retrieval.py  --question_path <path_to_question_file> --source_path <path_to_source_folder> --output_path <path_to_output_file>
```

### Example
```
python Model/retrieval.py --question_path Test/questions_preliminary.json --source_path data --output_path pred_retrieve.json
```
