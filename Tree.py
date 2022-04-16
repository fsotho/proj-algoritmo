from collections import defaultdict
import requests as rq

# Classe 

class Trie():
    
    def __init__(self):
        self.root=RadixTreeNode()

    # Transforma lista de palavras word_list em arvore

    def add_wordlist(self, word_list):
        for word in word_list:
            self.add_word(self.root, word)
        return True

    # 
    def add_word(self,node,word):
        for key, child in node.child_nodes.items():
            prefix, split, rest = self.match(key, word)
            if not split:
                #key complete match
                if not rest:
                    #word matched
                    child.word=True
                    return True
                else:
                    #match rest of word
                    return self.add_word(child, rest)
                    
            if prefix:
                #key partial match, need to split
                new_node = RadixTreeNode(word=not rest,keys={split:child})
                node.child_nodes[prefix]=new_node
                del node.child_nodes[key]
                return self.add_word(new_node, rest)
        node.child_nodes[word] = RadixTreeNode(word=True)

    # 
    def search_word(self, word, node = False):
        if node == False:
            node = self.root
            
        for key,child in node.child_nodes.items():
            prefix, split, rest = self.match(key, word)
            if not split and not rest:
                return child
            if not split:
                return self.search_word(word = rest,node = child)
        return False
    

    # Busca da palavra na lista do url definida
    def add_url(self, url):
        
        text = rq.get(url).text
        text = text.replace("\n","").replace("\r","").replace("\ufeff","").upper()
        word_list = text.split(" ")
        
        for word in word_list:
            child = self.search_word(word)
            if child != False:
                child.add_url(url)
    
    # 
    def display_word(self, word):
        child = self.search_word(word)
        if child == False:
            print("Palavra não localizada")
            return True
        print("Palavra existe na Arvore")
        
        child.print_urls()
        return True
    
    # 
    def match(self, key, word):
        i=0
        for k,w in zip(key,word):
            if k!=w:
                break
            i+=1
        return key[:i],key[i:],word[i:]


# Classe RadixTreeNode

class RadixTreeNode():

    # Inicializando variaveis e seus valores
    def __init__(self, word = False, keys=None):
        
        self.word= word
        self.child_nodes = keys if keys else defaultdict(RadixTreeNode)
        self.url_list = []

    # Definindo função add url
    def add_url(self, url):
        if url not in self.url_list:
            self.url_list.append(url)
        return True
    
    # Definindo função de print
    def print_urls(self):
        if len(self.url_list) == 0:
            print("Nenhuma URL encontrada com essa palavra")
            return False
        print("Mostrando URLS:")
        for url in self.url_list:
            print(url)
        print("")
        return True