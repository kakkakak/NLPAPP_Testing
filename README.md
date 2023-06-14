# NLPTesting

## Python版本

- python 3.10

## 安装包

- jieba

- networkx
- nltk
- LAC
- stanfordcorenlp
- synonyms
- tensorflow
- transformers
- treelib
- pattern
- pyltp
- pytorch
- xlsxwriter
- stanfordcorenlp
- argparse

## 安装模型

- ltp-models 3.4.0
- Stanford Corenlp 
  - stanford-corenlp-4.5.4
  - Chinese models

## 步骤
### 预处理文本

- **python DerivationTree.py --file-name XXXX --Mtype XXXX**

- file-name：Data/Seeds文件夹中的文件名

- Mtype：mlm（掩码语言模型预测）；sys（同义词替换）

### SSM任务

- **python Experiment_SSM.py --file-name XXXX**

- file-name：Data/DerivationTree文件夹中的文件名

### MT任务

- 首先开启 Stanford Corenlp 服务：https://github.com/nltk/nltk/wiki/Stanford-CoreNLP-API-in-NLTK

- **python Experimet_MT.py --file-name XXXX --sid X --eid X**
- file-name：Data/DerivationTree文件夹中的文件名
- sid：开始的句子序号
- eid：结束的句子序号

