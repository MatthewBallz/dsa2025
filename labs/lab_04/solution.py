class Stack:
    def push(self, value):
        pass

    def pop(self):
        pass

    def peek(self):
        pass

    def isEmpty(self):
        pass


class Queue:
    def enqueue(self, value):
        pass

    def dequeue(self):
        pass

    def peek(self):
        pass

    def isEmpty(self):
        pass


class Deque:
    def pushFront(self, value):
        pass

    def pushBack(self, value):
        pass

    def popFront(self):
        pass

    def popBack(self):
        pass

    def peekFront(self):
        pass

    def peekBack(self):
        pass

    def isEmpty(self):
        pass


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class DoubleNode(Node):
    def __init__(self, value):
        super().__init__(value)
        self.prev = None


class ArrayStack(Stack):
    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)

    def pop(self):
        if self.isEmpty():
            return None
        return self.items.pop()

    def peek(self):
        if self.isEmpty():
            return None
        return self.items[-1]

    def isEmpty(self):
        return len(self.items) == 0


class LinkedStack(Stack):
    def __init__(self):
        self.head = None

    def push(self, value):
        node = Node(value)
        node.next = self.head
        self.head = node

    def pop(self):
        if self.isEmpty():
            return None
        value = self.head.value
        self.head = self.head.next
        return value

    def peek(self):
        if self.isEmpty():
            return None
        return self.head.value

    def isEmpty(self):
        return self.head is None


class ArrayQueue(Queue):
    def __init__(self):
        self.items = []

    def enqueue(self, value):
        self.items.append(value)

    def dequeue(self):
        if self.isEmpty():
            return None
        return self.items.pop(0)

    def peek(self):
        if self.isEmpty():
            return None
        return self.items[0]

    def isEmpty(self):
        return len(self.items) == 0


class LinkedQueue(Queue):
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, value):
        node = Node(value)
        if self.isEmpty():
            self.head = node
        else:
            self.tail.next = node
        self.tail = node

    def dequeue(self):
        if self.isEmpty():
            return None
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return value

    def peek(self):
        if self.isEmpty():
            return None
        return self.head.value

    def isEmpty(self):
        return self.head is None


class ArrayDeque(Deque):
    def __init__(self):
        self.items = []

    def pushFront(self, value):
        self.items.insert(0, value)

    def pushBack(self, value):
        self.items.append(value)

    def popFront(self):
        if self.isEmpty():
            return None
        return self.items.pop(0)

    def popBack(self):
        if self.isEmpty():
            return None
        return self.items.pop()

    def peekFront(self):
        if self.isEmpty():
            return None
        return self.items[0]

    def peekBack(self):
        if self.isEmpty():
            return None
        return self.items[-1]

    def isEmpty(self):
        return len(self.items) == 0


class LinkedDeque(Deque):
    def __init__(self):
        self.head = None
        self.tail = None

    def pushFront(self, value):
        node = DoubleNode(value)
        node.next = self.head
        if self.isEmpty():
            self.tail = node
        else:
            self.head.prev = node
        self.head = node

    def pushBack(self, value):
        node = DoubleNode(value)
        node.prev = self.tail
        if self.isEmpty():
            self.head = node
        else:
            self.tail.next = node
        self.tail = node

    def popFront(self):
        if self.isEmpty():
            return None
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
        return value

    def popBack(self):
        if self.isEmpty():
            return None
        value = self.tail.value
        self.tail = self.tail.prev
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None
        return value

    def peekFront(self):
        if self.isEmpty():
            return None
        return self.head.value

    def peekBack(self):
        if self.isEmpty():
            return None
        return self.tail.value

    def isEmpty(self):
        return self.head is None

def check_brackets(text):
    stack = ArrayStack()
    pairs = {')': '(', ']': '[', '}': '{'}
    correct = True

    for bracket in text:
        if bracket in '([{':
            stack.push(bracket)
        elif bracket in pairs:
            if stack.isEmpty() or stack.pop() != pairs[bracket]:
                correct = False
                break
        else:
            correct = False
            break

    if not stack.isEmpty():
        correct = False
    if not correct:
        print('Ошибка в скобочной последовательности:', text)
    return correct


def evaluate_postfix(text):
    stack = ArrayStack()

    for symbol in text:
        if symbol.isspace():
            continue
        if symbol in '123456789':
            stack.push(int(symbol))
        else:
            right = stack.pop()
            left = stack.pop()
            if symbol == '+':
                result = left + right
            elif symbol == '-':
                result = left - right
            elif symbol == '*':
                result = left * right
            else:
                result = left / right
            stack.push(result)

    if stack.isEmpty():
        print('Нет результата вычисления')
        return None
    result = stack.pop()
    if not stack.isEmpty():
        print('В выражении лишние числа')
        return None
    return result


def infix_to_postfix(text):
    stack = ArrayStack()
    output = []
    priority = {'+': 1, '-': 1, '*': 2, '/': 2}

    for symbol in text:
        if symbol.isspace():
            continue
        if symbol in '123456789':
            output.append(symbol)
        elif symbol == '(':
            stack.push(symbol)
        elif symbol == ')':
            while not stack.isEmpty() and stack.peek() != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while not stack.isEmpty() and stack.peek() != '(':
                if priority[stack.peek()] < priority[symbol]:
                    break
                output.append(stack.pop())
            stack.push(symbol)

    while not stack.isEmpty():
        output.append(stack.pop())
    return ''.join(output)


if __name__ == '__main__':
    for stack_type in (ArrayStack, LinkedStack):
        stack = stack_type()
        stack.push(1)
        stack.push(2)
        print(stack_type.__name__, stack.pop(), stack.pop())

    for queue_type in (ArrayQueue, LinkedQueue):
        queue = queue_type()
        queue.enqueue(1)
        queue.enqueue(2)
        print(queue_type.__name__, queue.dequeue(), queue.dequeue())

    for deque_type in (ArrayDeque, LinkedDeque):
        deque = deque_type()
        deque.pushFront(1)
        deque.pushBack(2)
        print(deque_type.__name__, deque.popFront(), deque.popBack())

    for text in ('([]{})', '([)]', '(('):
        print(text, check_brackets(text))

    print('23+4* =', evaluate_postfix('23+4*'))
    for text in ('2+3*4', '(2+3)*4', '8-3-2'):
        postfix = infix_to_postfix(text)
        print(text, '->', postfix, '=', evaluate_postfix(postfix))
