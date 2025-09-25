class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.head = None
        self.count = 0
        
    def is_empty(self):
        return self.head is None
    
    def push(self, item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node
        self.count += 1

    def pop(self):
        if not self.is_empty():
            value = self.head.value
            self.head = self.head.next
            self.count -= 1
            return value
        return None

    def peek(self):
        if not self.is_empty():
            return self.head.value
        return None

    def size(self):
        return self.count

def are_parentheses_balanced(expression):
    s = Stack()
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in expression:
        if char in mapping.values():  # It's an opening parenthesis
            s.push(char)
        elif char in mapping.keys():  # It's a closing parenthesis
            if s.is_empty() or s.pop() != mapping[char]: 
                return False
    
    return s.is_empty()

if __name__ == "__main__":
    # Example usage:
    expression1 = "([{}])"
    expression2 = "({[})"

    print(f"'{expression1}' is balanced: {are_parentheses_balanced(expression1)}") # Expected: True
    print(f"'{expression2}' is balanced: {are_parentheses_balanced(expression2)}") # Expected: False