# Definindo a classe da pilha
class Stack:
    def __init__(self):
        self.items = []

    # Adicionando um elemento na pilha
    def push(self, item):
        self.items.append(item)

    # Removendo e retornando o elemento no topo da pilha
    def pop(self):
        return self.items.pop()

    # Verificando se a pilha está vazia
    def is_empty(self):
        return len(self.items) == 0

# Testes: Criando uma pilha e realizando operações

#stack = Stack()
#stack.push(1)
#stack.push(2)
#stack.push(3)
#print(stack.pop()) # Output: 3
#print(stack.is_empty()) # Output: False

# Se removermos todos os elementos utilizando o seguinte código: 
#print(stack.pop()) # Output: 2
#print(stack.pop()) # Output: 1
# Teremos uma fila vazia. Desse modo, teremos a condição de "empty" atendida. 
# print(stack.is_empty()) # Output: True