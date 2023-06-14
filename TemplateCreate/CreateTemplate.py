from TemplateCreate.SentenceData import SentenceData
from TemplateCreate.ExtractComponents import extract_components
from TemplateCreate.CompressSentence import compress_sentence


def create_template(sentence):
    data = SentenceData(sentence)
    extract_components(data)
    adjuncts = compress_sentence(data)
    return data.WordsPos, adjuncts


if __name__ == '__main__':
    sentence1 = 'On May 3, downtown Jacksonville was ravaged by a fire that started as a kitchen fire.'
    sentence2 = "He could not produce all his power in the previous performances because he needed to save energy for the jumps."
    create_template(sentence2)


