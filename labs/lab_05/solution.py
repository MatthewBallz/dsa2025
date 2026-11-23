import hashlib
import json


class ChainedHashTable:
    def __init__(self, size=8):
        if size < 1:
            raise ValueError("Размер должен быть положительным")
        self.buckets = []
        for i in range(size):
            self.buckets.append([])
        self.count = 0

    def _bucket(self, key):
        index = hash(key) % len(self.buckets)
        return self.buckets[index]

    def insert(self, key, value):
        bucket = self._bucket(key)
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.count += 1
        if self.count > 0.75 * len(self.buckets):
            self._resize()

    def _resize(self):
        old = self.buckets
        new_size = 2 * len(old)
        self.buckets = []
        for i in range(new_size):
            self.buckets.append([])
        for bucket in old:
            for entry in bucket:
                new_bucket = self._bucket(entry[0])
                new_bucket.append(entry)

    def get(self, key):
        for entry in self._bucket(key):
            if entry[0] == key:
                return entry[1]
        return None

    def delete(self, key):
        bucket = self._bucket(key)
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket.pop(i)
                self.count -= 1
                return True
        return False


class OpenHashTable:
    DELETED = object()

    def __init__(self, size=8):
        if size < 1:
            raise ValueError("Размер должен быть положительным")
        self.slots = []
        for i in range(size):
            self.slots.append(None)
        self.count = 0
        self.used = 0

    def _find_slot(self, key):
        size = len(self.slots)
        start = hash(key) % size
        first_deleted = None
        for step in range(size):
            i = (start + step) % size
            entry = self.slots[i]
            if entry is None:
                if first_deleted is None:
                    return i
                return first_deleted
            if entry is self.DELETED:
                if first_deleted is None:
                    first_deleted = i
            elif entry[0] == key:
                return i
        return first_deleted

    def insert(self, key, value):
        i = self._find_slot(key)
        if self.slots[i] is None:
            self.used += 1
        if self.slots[i] is None or self.slots[i] is self.DELETED:
            self.count += 1
        self.slots[i] = (key, value)
        if self.used > 0.75 * len(self.slots):
            self._rehash()

    def _rehash(self):
        old = self.slots
        size = len(old)
        if self.count > size // 2:
            size *= 2
        self.slots = []
        for i in range(size):
            self.slots.append(None)
        for entry in old:
            if entry is not None and entry is not self.DELETED:
                index = self._find_slot(entry[0])
                self.slots[index] = entry
        self.used = self.count

    def get(self, key):
        entry = self.slots[self._find_slot(key)]
        if entry is None or entry is self.DELETED:
            return None
        return entry[1]

    def delete(self, key):
        i = self._find_slot(key)
        if self.slots[i] is None or self.slots[i] is self.DELETED:
            return False
        self.slots[i] = self.DELETED
        self.count -= 1
        return True


class Block:
    def __init__(self, data, previous_hash):
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        fields = json.dumps([self.data, self.previous_hash], ensure_ascii=False)
        encoded = fields.encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


class Blockchain:
    def __init__(self):
        self.blocks = []

    def add_block(self, data):
        previous = "0"
        if len(self.blocks) > 0:
            last_block = self.blocks[-1]
            previous = last_block.hash
        block = Block(data, previous)
        self.blocks.append(block)

    def is_valid(self):
        previous = "0"
        for block in self.blocks:
            if block.previous_hash != previous or block.hash != block.calculate_hash():
                return False
            previous = block.hash
        return True


def intersect(first, second):
    seen = set()
    for item in first:
        seen.add(item)
    for item in second:
        if item in seen:
            return True
    return False


def all_unique(items):
    seen = set()
    for item in items:
        if item in seen:
            return False
        seen.add(item)
    return True


def find_pairs(numbers, target):
    seen = set()
    pairs = []
    added = set()
    for number in numbers:
        other = target - number
        if other in seen:
            pair = (min(number, other), max(number, other))
            if pair not in added:
                pairs.append(pair)
                added.add(pair)
        seen.add(number)
    return pairs


def are_anagrams(first, second):
    if len(first) != len(second):
        return False
    counts = {}
    for char in first:
        if char not in counts:
            counts[char] = 0
        counts[char] += 1
    for char in second:
        if char not in counts or counts[char] == 0:
            return False
        counts[char] -= 1
    return True


if __name__ == "__main__":
    tables = [ChainedHashTable(), OpenHashTable()]
    for table in tables:
        table.insert(1, "один")
        table.insert(9, "девять")
        table.delete(1)
        print(type(table).__name__, table.get(1), table.get(9))

    chain = Blockchain()
    chain.add_block("Первая запись")
    chain.add_block("Вторая запись")
    print("Исходная цепочка:", chain.is_valid())
    chain.blocks[0].data = "Исправленная запись"
    print("После изменения:", chain.is_valid())

    print("Пересечение [1, 4] и [3, 4]:", intersect([1, 4], [3, 4]))
    print("Все элементы [2, 5, 2] уникальны:", all_unique([2, 5, 2]))
    print("Пары с суммой 6:", find_pairs([1, 5, 3, 3, 5, -1, 7], 6))
    print("«пила» и «липа» — анаграммы:", are_anagrams("пила", "липа"))
