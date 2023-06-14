from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd
import argparse


tokenizer = AutoTokenizer.from_pretrained("ModelTC/bert-base-uncased-qqp")
model = AutoModelForSequenceClassification.from_pretrained("ModelTC/bert-base-uncased-qqp")
classes = ["0", "1"]


def semantic_similarity(sent_1, sent_2):
    test = tokenizer.encode_plus(sent_1, sent_2, return_tensors="pt")
    test_classification_logits = model(**test)[0]
    test_results = torch.softmax(test_classification_logits, dim=1)
    similarity_result = torch.argmax(test_results, dim=1)
    label = classes[similarity_result]
    return label

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-name',
                        default='ssm')
    return parser.parse_args()


def main():
    args = parse_args()
    file_name = args.file_name
    pred_file = './Data/DerivationTree/' + file_name + '_pred.txt'
    test_file = './Data/Experiment_SSM/' + file_name + '_bug.txt'
    r = open(pred_file, mode='r', encoding='utf-8')
    w = open(test_file, mode='a', encoding='utf-8')
    num_error = 0
    num = 0
    line = r.readline()
    sent_id = -1
    sent_level = -1
    sents_list = []
    sent_pa = ""
    while line:
        if line.startswith("sent_id"):
            sent_id = line.lstrip("sent_id  = ").rstrip("\n")
            sent_level = -1 # basic structure
        elif line.startswith("add"):
            sent_level = int(line.lstrip('add [').rstrip(']\n'))
        elif line.startswith("FIN"):
            sents_list.clear()
            print("end sent {}".format(sent_id))
        elif line == '\n':
            sent_pa = sents_list.pop(0)
        else:
            if int(sent_level) == -1:
                sent_pa = line.rstrip('\n')
            else:
                sent = line.rstrip('\n')
                sents_list.append(sent)
                num += 1
                label = semantic_similarity(sent_pa, sent)
                if int(label) == 1:
                    num_error += 1
                    w.write("sent {} add {}:".format(sent_id, sent_level) + ": " + sent_pa + '\t' + sent + '\n')
        line = r.readline()
    r.close()
    w.close()
    print("num error: {}    total num: {}".format(num_error, num))


if __name__ == '__main__':
    main()




