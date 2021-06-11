# Writer      : eddie Lopez
# Author      : Alfrick Opidi
# Date        : 30 April 2021
# Last updated: 31 May 2021
# For         : TechRes A
# Notes       : comments in green explaining everything (which may be super helpful to non-python users). Also, pulled this from an online tutorial (which is why there is both a "writer" and "author" label). Will use this as a proof of concept. Probably rewrite later with a better model and then can claim authorship at that point. Using this more so to understand.

# first step is to import the neccesary libraries... which for this, are for the hash and for time
import hashlib
import time

# next, we create a class titled "Block". 
# Class = code template for creating object; have member variables and behaviors associated with them
# ":" tells python where to slice and that something is a part of the thing beneath it; indents the block

class Block:
    
    # "def" = define. How python creates functions
    # "__init__" is a constructor; it initializes the attributes of a class
    def __init__(self, index, proof_no, prev_hash, data, timestamp=None):
        # "self" = referes to the instance of the Block class, making it possible to access the methods and attributes associated with the class
        self.index = index #keeps track of the position within the blockchain
        self.proof_no = proof_no #this is the number produced during the creation of the block (called mining)
        self.prev_hash = prev_hash #this refers to the hash of the previous block within the chain
        self.data = data #this gives a record of all transactions completed, such as the quantity bought
        self.timestamp = timestamp or time.time() #places a timestamp for the transactions

    # "@"  symbol at the beginning of a line is used for class, function, and method decorators
    # decorator = the name used for a software design pattern; dynamically alters the functionality of a function, method, or class without having to directly use subclasses or change the source code of the function being decorated
    # "property" = a pythonic way to use getters and setters in object-oriented programming
    @property 
    # will generate the hash of the block using the above values
    def calculate_hash(self):
        block_of_string = "{}{}{}{}{}".format(self.index, self.proof_no, self.prev_hash, self.data, self.timestamp)

        # ".sha256" = designates the return will be a 256-bit string representing the contents of the block
        return hashlib.sha256(block_of_string.encode()).hexdigest()

    # "__repr__" = a special method used to represent a class's objects as a string
    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self.index, self.proof_no, self.prev_hash, self.data, self.timestamp)

# creating a new class to manage the workings of the whole chain
class BlockChain:
    def __init__(self):
        self.chain = [] #this variable keeps all blocks
        self.current_data = [] #this variable keeps all the completed transactions in the block
        self.nodes = set()  #this variable sets the nodes
        self.construct_genesis() #this method will take care of constructing the initial block; different than other blocks because it symbolizes the start of the blockchain

    def construct_genesis(self): #doing what I said above
        self.construct_block(proof_no=0, prev_hash=0) #zero is a filler number; numbers can be any value
    
    def construct_block(self, proof_no, prev_hash): #code for constructing new blocks in the chain
        block = Block(
            index=len(self.chain), #length of the block
            proof_no=proof_no, #as defined above
            prev_hash=prev_hash, #as defined above
            data=self.current_data) #record of transactions outside of the blocks on the node
        self.current_data = [] #resets transactions list on node

        self.chain.append(block) #method adds the newly constructed blocks to the chain
        return block #newly constructed object is returned
    
    @staticmethod
    def check_validity(block, prev_block): #assesses the integrity of the blockchain; checks if every hash of the block is correct and that each block is properly linked to the previous block
        if prev_block.index + 1 != block.index: #checks placement of block in the chain
            return False

        elif prev_block.calculate_hash != block.prev_hash: #checks hash of block
            return False

        elif not BlockChain.verifying_proof(block.proof_no, prev_block.proof_no): #compares the proof numbers
            return False

        elif block.timestamp <= prev_block.timestamp: #checks the timestamp
            return False
        
        return True #if none of these errors occur (meaning none of the stuff we checked for above), return "True"

    def new_data(self, sender, recipient, quantity): #adds the data of transactions to the block
        self.current_data.append({
            'sender': sender, #sender's info
            'recipient': recipient, #recipient's info
            'quantity': quantity #quantity sent
        })
        return True

    @staticmethod
    def proof_of_work(last_proof): #this is the problem that the code is trying to solve that gives the blockchain its value
    #here are some notes from the author on the problem that is taking place here (supposedly a "simple" algorithm, with notes from the author in quotes)
        #This algorithm "identifies a number f' such that hash (ff') contain 4 leading zeroes
        #f is the previous f'
        #f' is the new proof"

        proof_no = 0
        while BlockChain.verifying_proof(proof_no, last_proof) is False:
            proof_no += 1
        
        return proof_no
    
    @staticmethod
    def verifying_proof(last_proof, proof): #"does hash(last_proof, proof) contain 4 leading zeroes?

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @property
    def latest_block(self): #how we obtain the last block in the blockchain (which is actually the current block in the chain)
        return self.chain[-1]
    
    def block_mining(self, details_miner):

        self.new_data(
            sender="0",
            receiver=details_miner,
            quantity=
            1,
        )

        last_block = self.latest_block

        last_proof_no = last_block.proof_no
        proof_no = self.construct_block(proof_no, last_hash)

        return vars(block)
        
    def create_node(self, address):
        self.nodes.add(address)
        return True

    @staticmethod
    def obtain_block_object(block_data):

        return Block(
            block_data['index'],
            block_data['proof_no'],
            block_data['prev_hash'],
            block_data['data'],
            timestamp=block_data['timestamp'])


# now let us test this code...
blockchain = BlockChain()

print("***Mining TNLcoin about to start***")
print(blockchain.chain)

last_block = blockchain.latest_block
last_proof_no = last_block.proof_no
proof_no = blockchain.proof_of_work(last_proof_no)

blockchain.new_data(
    sender="0", #it implies that this node has created a new block
    recipient="Aaron Lucas", #assigning the TNL coin to Aaron
    quantity=
    1, #creating a new block (or identifying the proof number) is awarded with 1
)

last_hash = last_block.calculate_hash
block = blockchain.construct_block(proof_no, last_hash)

print("***Mining TNLcoin has been successful***")
print(blockchain.chain)
