class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class MessageQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, message):
        new_node = Node(message)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        return f"Enqueued: '{message}'"

    def dequeue(self):
        if not self.is_empty():
            message = self.head.value
            self.head = self.head.next
            if self.head is None: # If the queue becomes empty
                self.tail = None
            self.size -= 1
            return f"Delivered \u2192 '{message}'"
        return "Queue is empty. No message to dequeue."

    def is_empty(self):
        return self.head is None
    def display_queue(self):
        if self.is_empty():
            return "Remaining Queue: []"
        
        current = self.head
        queue_elements = []
        while current:
            queue_elements.append(current.value)
            current = current.next
        return f"Remaining Queue: {queue_elements}"

if __name__ == "__main__":
    mq = MessageQueue()

    print("Messaging Queue Simulation")
    print("1. Enqueue a message")
    print("2. Dequeue a message")
    print("3. Display current queue")
    print("4. Exit")

    while True:
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            message = input("Enter message to enqueue: ")
            print(mq.enqueue(message))
        elif choice == "2":
            print(mq.dequeue())
        elif choice == "3":
            print(mq.display_queue())
        elif choice == "4":
            print("Exiting Message Queue Simulator.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
