# Definindo a classe da fila
class Queue:
    def __init__(self):
        self.items = []

    # Adicionando um elemento na fila
    def enqueue(self, item):
        self.items.append(item)

    # Removendo e retornando o elemento no início da fila
    def dequeue(self):
        return self.items.pop(0)

    # Verificando se a fila está vazia
    def is_empty(self):
        return len(self.items) == 0

# Testes: Criando uma fila e realizando operações
#pontos = Queue()
#pontos.enqueue([0.0, 0.5])
#pontos.enqueue([0.5, 0.0])
#pontos.enqueue([0.0, 0.5])
#pontos.enqueue([0.5, 0.0])
#pontos.enqueue([0.0, 1.0])
#pontos.enqueue([1.0, 0.0])
#print(queue.dequeue())