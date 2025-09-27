class Stack:
    def __init__(self):
        self.items = []
        
    def is_empty(self):
        return len(self.items) == 0
    
    
    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def size(self):
        return len(self.items)

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
