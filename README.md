# Data Structures Implementation: Stack and Message Queue
*A Python implementation of Stack and Message Queue using linked list data structure*

## Overview
This repository contains two main implementations:
1. **Stack with Parentheses Checker**: A linked list-based stack implementation with a parentheses balancing checker
2. **Message Queue**: A linked list-based message queue implementation with a simple console interface

## Stack Implementation (`stack_linked_list.py`)
### Features
- Linked list-based stack implementation
- Basic stack operations: push, pop, peek
- Size tracking and empty state checking
- Parentheses balancing checker utility
- Supports (), [], and {} brackets

### Usage Example
```python
# Create a new stack
stack = Stack()

# Check if parentheses are balanced
expression = "([{}])"
result = are_parentheses_balanced(expression)
print(f"'{expression}' is balanced: {result}")  # True
```

## Message Queue Implementation (`messagingqueue.py`)
### Features
- Linked list-based queue implementation
- Basic queue operations: enqueue, dequeue
- Queue display functionality
- Interactive console interface
- Size tracking and empty state checking

### Usage Example
```python
# Create a new message queue
mq = MessageQueue()

# Enqueue a message
mq.enqueue("Hello World!")

# Dequeue a message
message = mq.dequeue()

# Display current queue
print(mq.display_queue())
```

## Installation
1. Clone the repository:
```bash
git clone https://github.com/rahul200618/OOPS.git
```

2. Navigate to the project directory:
```bash
cd OOPS
```

## How to Run
### Stack Implementation
```bash
python stack_linked_list.py
```

### Message Queue
```bash
python messagingqueue.py
```

## Time Complexity
### Stack Operations
- Push: O(1)
- Pop: O(1)
- Peek: O(1)
- isEmpty: O(1)

### Queue Operations
- Enqueue: O(1)
- Dequeue: O(1)
- Display: O(n)
- isEmpty: O(1)

## Contributing
Feel free to submit issues and enhancement requests!

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Author
[rahul200618](https://github.com/rahul200618)