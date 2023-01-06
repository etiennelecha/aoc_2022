with open('aoc_day20.txt', 'r') as f:
    nums = list(map(int, f.read().splitlines()))

class DLNode:
    def __init__(self, val, prev=None, next=None, og_idx= -1):
        self.val = val
        self.prev = prev
        self.next = next
        self.og_idx = og_idx
    
    @staticmethod
    def build(nums):
        nodes = [DLNode(nums[0], og_idx= 0)]
        for i in range(1, len(nums)):
            node = DLNode(nums[i], prev= nodes[i - 1], og_idx = i)
            nodes[i - 1].next = node
            nodes.append(node)
        nodes[-1].next = nodes[0]
        nodes[0].prev = nodes[-1]
        return nodes
    
    def __repr__(self):
        return f'og index: {self.og_idx}'

class PartI:
    @staticmethod
    def mix(nodes):
        n = len(nodes)
        for head in nodes:
            steps = head.val
            ptr = head 
            step = 0
            if abs(steps) % (n - 1) == 0 or - abs(steps) % (n - 1) == 0:
                continue
            if steps > 0:
                while step < steps % (n - 1):
                    ptr = ptr.next
                    step += 1
            elif steps < 0:
                while step < (-steps) % (n - 1):
                    ptr = ptr.prev
                    step += 1
            head.prev.next = head.next
            head.next.prev = head.prev
            if steps > 0:
                tmp = ptr.next
                head.prev = ptr
                head.next = tmp
                ptr.next = head
                tmp.prev = head
            elif steps < 0:
                tmp = ptr.prev
                head.next = ptr
                head.prev = tmp
                ptr.prev = head
                tmp.next = head
    
    def __call__(self):
        nodes = DLNode.build(nums)
        n = len(nodes)
        PartI.mix(nodes)
        i0 = - 1
        for j in range(n):
            if nums[j] == 0:
                i0 = j
                break
        mix = []
        ptr = nodes[i0]
        for _ in range(n):
            if ptr:
                mix.append(ptr.val)
                ptr = ptr.next

        return sum((mix[1000 % n], mix[2000 % n], mix[3000 % n]))

class PartII:
    def __call__(self):
        KEY = 811589153
        nums_2 = list(map(lambda x: x * KEY, nums))
        nodes = DLNode.build(nums_2)
        n = len(nodes)
        for _ in range(10):
            PartI.mix(nodes)
        i0 = -1
        for j in range(n):
            if nums[j] == 0:
                i0 = j
                break
        mix = []
        ptr = nodes[i0]
        for _ in range(n):
            if ptr:
                mix.append(ptr.val)
                ptr = ptr.next

        return sum((mix[1000 % n], mix[2000 % n], mix[3000 % n]))

if __name__ == '__main__':
    print(PartI()())
    print(PartII()())