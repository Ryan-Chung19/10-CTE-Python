import spacy

class NLP():
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def showDoc(self, doc):
        for token in doc:
            print(f"{token.text:10s}, {token.lemma_:12s}, {token.pos_:10s}, {token.tag_:10s}, {token.dep_:10s}, {token.shape_:12s}, {token.is_alpha}, {token.is_stop}")

    def getNameByPartsOfSpeech(self, speech):
        names = []
        doc = self.nlp(speech)
        self.showDoc(doc)
        for token in doc:
            if token.pos_ in ["PROPN"]:
                names.append(token.text)
        
        name = " ".join(names)
        return name
    
    # def getNounsByPartsOfSpeech()

    def getNameByEntityType(self, speech):
        names = []
        doc = self.nlp(speech)
        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)

            if ent.label_ == 'PERSON':
                names.append(ent.text)

        name = " ".join(names)
        return name 


def main():
    nlpDemo = NLP()

    sentence = ''

    # name = nlpDemo.getNameByPartsOfSpeech(sentence)
    # print(f'>>> Name By Speech found: {name}')

    names = nlpDemo.getNameByEntityType(sentence)
    for name in names:
        print(f">>> Name By Entity: {name}")

main()