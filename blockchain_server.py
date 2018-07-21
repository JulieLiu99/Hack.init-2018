from flask import Flask, request
from hashlib import sha256
import time
import json
import requests
from random import randint


# Block class is the most basic storing unit
# in a Blockchain. 
class Block:
    def __init__(self, index, transactions, time_stamp, previous_hash):
        self.index = index
        # by convention, data within a blockchain
        # is called transactions. Here type(transactions)==dict
        self.transactions = transactions
        self.time_stamp = time_stamp
        # blockchain are linked with hash values
        self.previous_hash = previous_hash

    # json.dumps automatically format a json file into a string
    # sha256 is a strong way to generate a hash value with 64 chars
    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


# Blockchain class connects all blocks to a
# whole chain
#
# **class methods:
# **void create_genesis_block(self)
# **void last_block(self): when call call instance.last_block
# **string proof_of_work(self, block)
# **boolean add_block(self, block, proof)
# **boolean is_valid_proof(self, block, proof)
# **boolean add_transaction(self, transaction)
# **boolean check_chain_validity(self)
# **boolean check_transaction(self, transaction)
class Blockchain:
    def __init__(self):
        # where user's input data or file currently stored
        self.unconfirmed_transactions = {}
        # stores a chain of blocks, linked with hash values
        self.chain = []
        # each time we create a Blockchain we always want to
        # create a default genesis block 0
        self.create_genesis_block()

    # * input-None
    # * output-None
    # * generate a genesis block and append it into self.chain
    def create_genesis_block(self):
        genesis_block = Block(0, {}, time.time(), 0)
        genesis_block.hash = self.proof_of_work(genesis_block)
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    # * input-Block object
    # * output-Hash
    # * output a hash value meets constraints
    def proof_of_work(self, block):
        Blockchain.difficulty = 3
        block.nonce = 0
        computed_hash = block.compute_hash()
        # generates the hash until find a hash value that is valid
        while not computed_hash.startswith("0" * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    # * input-Block object, Hash
    # * output-boolean
    # * add a new Block to chain, return appending status
    def add_block(self, block, proof):
        previous_hash = self.last_block.hash 
        # if the to-be added block is invalid
        # return False without adding that block
        if (previous_hash != block.previous_hash
            ) or (not self.is_valid_proof(block, proof)):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    # * input-Block object, Hash
    # * output-boolean
    # * find out whether a Hash is eligible for this block
    def is_valid_proof(self, block, proof):
        return (proof.startswith("0" * Blockchain.difficulty) and 
            proof == block.compute_hash())

    # * input-None
    # * output-boolean
    # * check whether the current Blockchain is valid
    def check_chain_validity(self):
        previous_hash = 0
        # check the validity through Blockchain's base rule
        for block in self.chain:
            block_hash = block.hash
            delattr(block, "hash")
            if not self.is_valid_proof(block, block_hash) or\
                previous_hash != block.previous_hash:   
                return False
            block.hash, previous_hash = block_hash, block_hash
        return True

    # * input-dict
    # * output-boolean
    # * check whether submitted transaction is valid
    # !!!!!!!not debugged!!!!!!!
    def check_transaction(self, transaction):
        condition = []
        condition.append(transaction["type"] in ["pic", "trans"])
        condition.append("@" not in transaction["uploaded"][1:-1])
        condition.append(4 <= len(transaction) <= 5)
        return all(condition)

    # * input-dict
    # * output-boolean
    # * add unprocessed transaction to Blockchain, return status
    # !!!!!!!not debugged!!!!!!!
    def add_transaction(self, transaction):
        if type(transaction) == dict and self.check_transaction():
            self.unconfirmed_transactions = transaction
            return True
        else:
            return False

    # * input-None
    # * output-integer
    # * mine transactions to a new block
    # !!!!!!!not debugged!!!!!!!
    def mine(self):
        if not self.unconfirmed_transactions:
            return 0
        new_block = Block(self.last_block.index + 1,
                          self.unconfirmed_transactions,
                          time.time(),
                          self.last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = {}
        return new_block.index


        



# debug/test code
# def test():
#   bc = Blockchain()
#   time1 = time.time()
#   for i in range(10):
#       block = Block(bc.last_block.index+1, {randint(1,100):randint(1,100), randint(1,100):randint(1,100)}, time.time(), bc.last_block.hash)
#       bc.add_block(block,bc.proof_of_work(block))
#       print(bc.last_block.__dict__)
#       print(time.time()-time1)

#   print(bc.check_chain_validity())

# if __name__ == '__main__':
#   test()