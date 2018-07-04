import json

def add_word(word):
    with open('pybot/stopwords.json', 'r') as file:
        list_word = json.load(file)
        list_word.append(word)
    with open('pybot/stopwords.json', 'w', encoding='utf8') as file:
        list_word = json.dumps(list_word)
        file.write(list_word)

def main():
    word = ''
    while word != 'exit':
        word = input("Entrez un mot à ajouter ou 'exit' pour quitter : ")
        if word != 'exit':
            add_word(word)
            print('Le mot : "' + word + '"" a été ajouté à la liste ! ')
    print('Merci, à bientôt ! ')

if __name__ == "__main__":
    main()