from typing import Union, Optional
class Node:
    def __init__(self, value: Union[str, float], left: Optional['Node'] = None, right: Optional['Node'] = None):
        self.value = value
        self.left = left
        self.right = right



class ArbolDeEXpresiones:

    def __init__(self):
        self.root: Optional[Node] = None

    def print(self, node, prefix="", is_left=True):
        if not node:
          print("Empty Tree")
          return
        if node.right:
          self.print(node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + str(node.value))
        if node.left:
          self.print(node.left, prefix + ("    " if is_left else "│   "), True)

    def ValidarExpresion(self, expresion):
        operadores = ["+", "-", "*", "/", "^"]
        parentesis = 0
        corchetes = 0
        numeros = "0123456789"
        caracter_anterior = ""


        for i, caracter in enumerate(expresion):
            if caracter in operadores:
                if caracter_anterior and caracter_anterior in operadores:
                    return False

            if caracter in numeros:
                if caracter_anterior == ")" or caracter_anterior == "]":
                    return False

            if caracter == "(" or caracter == "[":
                if caracter_anterior and caracter_anterior in numeros:
                    print(caracter_anterior, caracter)
                    return False

            if caracter == "(":
                parentesis += 1
            if caracter == ")":
                if caracter_anterior == "(":
                    return False
                parentesis -= 1
                if parentesis < 0:
                    return False

            if caracter == "[":
                corchetes += 1
            if caracter == "]":
                corchetes -= 1
                if parentesis != 0:
                    return False
                if corchetes < 0:
                    return False
            caracter_anterior = caracter


        if parentesis !=0 or corchetes != 0:
            return False

        return True

    def ObtenerTokens(self, expresion):
        tokens = []
        current_number = ""

        for caracter in expresion:
            if caracter.isdigit() or caracter == '.':
                current_number += caracter
            else:
                if current_number:
                    tokens.append(current_number)
                    current_number = ""
                if caracter in "+-*/^()":
                    tokens.append(caracter)
        if current_number:
            tokens.append(current_number)


        return tokens

    def CrearArbol(self, expresion):
        if not self.ValidarExpresion(expresion):
            return

        tokens = self.ObtenerTokens(expresion)
        self.root = self.ConstruirArbol(tokens)


    def ConstruirArbol(self, tokens):
        PrioridadOperaciones = ['+', '-', '*', '/', '^']
        if tokens[0] == "(" and tokens[-1] == ")":
            tokens = tokens[1:-1]

        if len(tokens) == 1:
            return Node(float(tokens[0]))

        for operador in PrioridadOperaciones:


            indexOperador = self.IndiceOperadorPrincipal(operador, tokens)

            if indexOperador != False:
                tokens_izquierda_del_operador = tokens[:indexOperador]
                tokens_derecha_del_operador = tokens[indexOperador + 1:]

                return Node(
                    value=tokens[indexOperador],
                    left=self.ConstruirArbol(tokens_izquierda_del_operador),
                    right=self.ConstruirArbol(tokens_derecha_del_operador)
                    )


    def IndiceOperadorPrincipal(self, operador, tokens):


        parentesis = 0

        for i, token in enumerate(tokens):
            if token == '(':

                parentesis += 1
            elif token == ')':
                parentesis -= 1

            if parentesis == 0 and token == operador:
                return i
        return False



    def EvaluarExpresion(self, node=None):
        if node is None:
            node = self.root

        if node.left is None and node.right is None:
            return node.value

        if node.value == '+':
            return self.EvaluarExpresion(node.left) + self.EvaluarExpresion(node.right)

        elif node.value == '-':
            return self.EvaluarExpresion(node.left) - self.EvaluarExpresion(node.right)

        elif node.value == '*':
            return self.EvaluarExpresion(node.left) * self.EvaluarExpresion(node.right)

        elif node.value == '/':
            derecho = self.EvaluarExpresion(node.right)
            if derecho == 0:
                raise ValueError("Error: División por cero.")
            return self.EvaluarExpresion(node.left) / derecho

        elif node.value == '^':
            return self.EvaluarExpresion(node.left) ** self.EvaluarExpresion(node.right)



    def InOrder(self, current_node):
        if current_node is None:
            return ""

        subarbol_izquierdo = self.InOrder(current_node.left)
        current_value = str(current_node.value)
        subarbol_derecho = self.InOrder(current_node.right)

        if current_node.left and current_node.right:
            return f"({subarbol_izquierdo} {current_value} {subarbol_derecho})"
        return current_value


    def PostOrder(self, current_node):
        if current_node is None:
            return ""

        subarbol_izquierdo = self.PostOrder(current_node.left)
        subarbol_derecho = self.PostOrder(current_node.right)
        current_value = str(current_node.value)

        return f"{subarbol_izquierdo} {subarbol_derecho} {current_value}"


    def PreOrder(self, current_node):
        if current_node is None:
            return ""

        current_value = str(current_node.value)
        subarbol_izquierdo = self.PreOrder(current_node.left)
        subarbol_derecho = self.PreOrder(current_node.right)


        return f"{current_value} {subarbol_izquierdo} {subarbol_derecho}"


bst = ArbolDeEXpresiones()

expresion = "3+5*(4-7)+2-(900-100)"

bst.CrearArbol(expresion)

bst.print(bst.root)

print(bst.InOrder(bst.root))
print(bst.PreOrder(bst.root))
print(bst.PostOrder(bst.root))

print(bst.EvaluarExpresion(bst.root))


