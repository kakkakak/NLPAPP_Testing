from transformers import pipeline, AutoTokenizer, TFBertForMaskedLM
import string
import tensorflow as tf
import numpy as np

punc = string.punctuation

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
model = TFBertForMaskedLM.from_pretrained("bert-base-cased")


def get_mlm_word(masked_sent, orginal_word):
    predict_word_list = use_MaskedLM(masked_sent)
    if predict_word_list[0] != orginal_word:
        return 0, predict_word_list[0]
    else:
        return 1, predict_word_list[1]


def use_MaskedLM(masked_sent):
    predict_list = []
    inputs = tokenizer(masked_sent, return_tensors="tf")
    logits = model(**inputs).logits
    mask_token_index = tf.where((inputs.input_ids == tokenizer.mask_token_id)[0])
    selected_logits = tf.gather_nd(logits[0], indices=mask_token_index)
    predicted_token_id = tf.math.argmax(selected_logits, axis=-1)
    top_2 = tf.math.top_k(selected_logits, k=2).indices
    split = tf.split(top_2, axis=-1, num_or_size_splits=2)
    for s in split:
        predict_list.append(tokenizer.decode(int(s)))
    return predict_list

