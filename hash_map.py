# hash_map.py
# ===================================================
# Implementation of a hash map with chaining using linked lists
# ===================================================
# Author: Christine Pham

class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        del self._buckets[:]
        self.size = 0

    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """
        # make key case insensitive
        key = key.lower()

        # get the hash function the map was hashed with
        hashedKey = self._hash_function(key) % self.capacity
        thisBucketLL = self._buckets[hashedKey]

        cur = thisBucketLL.head

        # if the bucket isn't empty, traverse its linked list until you find a match
        if thisBucketLL.head is not None:
            while cur is not None:
                if cur.key == key:
                    return cur.value
                else:
                    cur = cur.next

        # if nothing found return None
        return None

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """
        # make an array big enough to temp store all the non-empty linked lists
        empty = self.empty_buckets()
        occ_buckets = self.capacity - empty
        temp = [LinkedList() for _ in range(occ_buckets)]

        # copy over all non-empty buckets into the temp list
        i = 0
        for lists in self._buckets:
            if lists.head is not None:
                cur = lists.head
                while cur is not None:
                    temp[i].add_front(cur.key, cur.value)
                    cur = cur.next
                i += 1
            else:
                continue

        # erase all linked lists
        self.clear()

        # change old capacity to new capacity
        self.capacity = capacity

        # change array size to new capacity
        for i in range(self.capacity):
            self._buckets.append(LinkedList())

        # grab a key within a bucket and rehash it to new capacity
        for ll in temp:
            cur = ll.head
            while cur is not None:
                hashedKey = self._hash_function(cur.key) % self.capacity
                newBucketLL = self._buckets[hashedKey]
                LinkedList.add_front(newBucketLL, cur.key, cur.value)
                self.size += 1
                cur = cur.next

    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """
        # make key case insensitive
        key = key.lower()

        hashedKey = self._hash_function(key) % self.capacity
        thisBucketLL = self._buckets[hashedKey]

        cur = thisBucketLL.head

        # if linked list at hashKey isn't empty
        if thisBucketLL.head is not None:
            while cur is not None:
                if cur.key == key:
                    # update the value if key already exists
                    cur.value = value
                    return
                else:
                    cur = cur.next
            # add to linked list if after traversing no matches
            LinkedList.add_front(thisBucketLL, key, value)

        else:
            # add to an empty bucket
            LinkedList.add_front(thisBucketLL, key, value)

        # update total amount of links in hash map
        self.size = 0
        for links in self._buckets:
            self.size += links.size

    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """
        # make key case insensitive
        key = key.lower()

        hashedKey = self._hash_function(key) % self.capacity
        thisBucketLL = self._buckets[hashedKey]

        # pass the key to be removed in the linked list class
        if thisBucketLL.head is not None:
            LinkedList.remove(thisBucketLL, key)

        # update total amount of links in hash map
        self.size = 0
        for links in self._buckets:
            self.size += links.size

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """
        # make key case insensitive
        key = key.lower()

        hashedKey = self._hash_function(key) % self.capacity
        thisBucketLL = self._buckets[hashedKey]

        if LinkedList.contains(thisBucketLL, key) is not None:
            return True
        return False

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        total = 0
        for hashedKeys in self._buckets:
            if hashedKeys.head is None:
                total += 1

        return total

    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        load = float(self.size / self.capacity)

        return round(load, 3)

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out
