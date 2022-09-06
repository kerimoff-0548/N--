import re
import pickle
import random
 
class Text():
    def __init__(self, filename):
        self.train = filename
 
    def fit(self):
        # читаем из файла, парсим текст, генерим биграммы, lowercase - предобработка
        with open(self.train, 'r', encoding='utf-8') as file:
            text = file.read()
 
        clean = re.sub('[^а-яё]', ' ', text.lower())
        split = re.split('\\s+', clean)
 
        word = {}
        for i in range(0, len(split) - 1):
            # исключаем повторения слов на стыках предложений
            if split[i] != split[i + 1]:
                if split[i] not in word:
                    word[split[i]] = [split[i + 1]]
                else:
                    if split[i + 1] not in word[split[i]]:
                        word[split[i]].append(split[i + 1])
 
        return pickle.dumps(word)
 
    def generate(self, length: int):
        bigrams = pickle.loads(self.fit())
 
        # в качестве первого слова будет идти то, после которого следует болше всего слов
        init_word = max(bigrams, key=lambda el: len(bigrams[el]))
        generat = [init_word]
        curr = init_word
        # генерируем новый текст длины length
        for i in range(length - 1):
            # выбираем случайно слово, следующее после текущего -> curr
            next = random.choice(bigrams[curr])
            generat.append(next)
            # обновляем текущее слово
            curr = next
 
        # создаем файл с новым текстом
        with open('generated.txt', 'w') as f:
            f.write(' '.join(generat))
        
def main():
    length = int(input('Enter the length of the string: '))
    filename = input('Enter the file name: ')

    print('\n\n\tWait for the program to run...')

    text_1 = Text(filename)
    text_1.generate(length)

    print('\n File generate.txt created')
 
if __name__ == '__main__':
    main()