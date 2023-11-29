import numpy as np
import time as time
from BitVector import *

Rcon = []
Sbox = (
0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
)
# convert Sbox to character numpy matrix
Sbox = np.frombuffer(bytes(Sbox), dtype=np.uint8).astype(np.uint8)
Sbox_inv = (
0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
)
# convert Sbox_inv to character numpy matrix
Sbox_inv = np.frombuffer(bytes(Sbox_inv), dtype=np.uint8).astype(np.uint8)

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]

AES_MODULUS = BitVector(bitstring='100011011')
BLOCK_LENGTH_IN_BYTES = 16

# for debugging and testing
def print_key_hex(key):
    for i in range(0, len(key)):
        print(hex(key[i]), end=" ")
    print()

def print_key_matrix_hex(key_matrix):
    print()
    for i in range(0, len(key_matrix)):
        for j in range(0, len(key_matrix[i])):
            print(hex(key_matrix[i][j]), end=" ")
        print()


# both use cases
def split_string_into_blocks(input_string, block_size=BLOCK_LENGTH_IN_BYTES):
    return [input_string[i:i+block_size] for i in range(0, len(input_string), block_size)]

def matrix_to_string(matrix):
    ascii_string = ""
    for i in range(0,len(matrix[0])):
        for j in range(0,len(matrix)):
            ascii_string += chr(matrix[j][i])
    return ascii_string  

# can be used for both mix_columns and inv_mix_columns
def mix_columns(state_matrix, inv=False):
    mixer = Mixer
    
    if inv:
        mixer = InvMixer

    result_matrix = np.zeros((4, 4), dtype=np.uint8)

    for i in range(0, len(state_matrix)):
        for j in range(0, len(state_matrix[i])):
            for k in range(0, len(state_matrix[i])):
                result_matrix[i][j] ^= mixer[i][k].gf_multiply_modular(BitVector(intVal=state_matrix[k][j], size=8), AES_MODULUS, 8).intValue()
                     

    return result_matrix

def bitwise_xor_string(string1, string2):
    bv1 = BitVector(textstring=string1)
    bv2 = BitVector(textstring=string2)

    bv3 = bv1 ^ bv2

    return bv3.get_bitvector_in_ascii()

def do_proper_padding(msg_blocks):
    # last block
    last_block = msg_blocks[-1]

    # if last block is full, add a new block of BLOCK_LENGTH_IN_BYTES=16 bytes, all 0s
    if len(last_block) == BLOCK_LENGTH_IN_BYTES:
        msg_blocks.append(chr(0) * BLOCK_LENGTH_IN_BYTES)
        return msg_blocks

    # if not full, add padding with each byte having value of number of bytes added
    padding_length = BLOCK_LENGTH_IN_BYTES - len(last_block)
    for _ in range(0, padding_length):
        # print(padding_length)
        last_block += chr(padding_length)
        
    msg_blocks[-1] = last_block

    return msg_blocks

def remove_proper_padding(msg_blocks):
    # last block
    last_block = msg_blocks[-1]

    # extract last byte, it is the number of bytes added, if it is 0, then remove the last block
    last_byte = ord(last_block[-1])
    if last_byte == 0:
        msg_blocks.pop()
        return msg_blocks
    
    # if not 0, then remove the last last_byte characters
    msg_blocks[-1] = last_block[:-last_byte]
    return msg_blocks


def get_next_round_key(key, round):
    # key is 4X4 numpy matrix
    # round is integer 1,2,3,4,5,6,7,8,9,10
    next_key = np.zeros((4, 4), dtype=np.uint8)

    g = np.copy(key[0:, 3])

    # rotate
    g = np.roll(g, -1)
    # substitute with Sbox
    for i in range(0, len(g)):
        g[i] = Sbox[g[i]]

    # xor with round_constant
    round_constant = np.array([Rcon[round - 1], 0, 0, 0], dtype=np.uint8)
    g = np.bitwise_xor(g, round_constant)
    g = np.reshape(g, (4, 1), order='F')
    
    # xor g with first column of key and store in first column next_key
    next_key[:, 0] = np.bitwise_xor(key[:, 0], g[:, 0])

    # xor with second column of key
    for i in range(1, len(key[0])):
        next_key[:, i] = np.bitwise_xor(key[:, i], next_key[:, i - 1])

    return next_key
    


# gets key as a 128 bit string and returns a 11 size array of 4X4 numpy matrices
def schedule_key(key):
    # key_matrix = np.reshape(np.frombuffer(key.encode('ascii'), dtype=np.uint8).astype(np.uint8), (4, 4), order='F')

    key_matrix = np.zeros((4, 4), dtype=np.uint8)
    for i in range(0, len(key)):
        key_matrix[i % 4][i // 4] = ord(key[i])

    # 11 size array of 4X4 numpy matrices
    key_matrices = np.zeros((11, 4, 4), dtype=np.uint8)
    key_matrices[0] = key_matrix

    for i in range(1, 11):
        key_matrices[i] = get_next_round_key(key_matrices[i - 1], i)

    return key_matrices

# encryption codes
# state_matrix, key_matrix are 4X4 numpy matrices
def AES_encrypt_round(state_matrix, key_matrix):
    # substritute bytes
    for i in range(0, len(state_matrix)):
        for j in range(0, len(state_matrix[i])):
            state_matrix[i][j] = Sbox[state_matrix[i][j]]

    # shift rows, shift ith row i times
    for i in range(0, len(state_matrix)):
        state_matrix[i] = np.roll(state_matrix[i], -i)
    # mix columns
    state_matrix = mix_columns(state_matrix)
    # add round key
    state_matrix = np.bitwise_xor(state_matrix, key_matrix)

    return state_matrix    


def aes_encrypt_block(scheduled_key, msg):
    # convert msg to 4X4 matrix
    # matrix is a 4X4 list
    # traverse matrix column wise and store msg character by character
    msg_matrix = np.zeros((4, 4), dtype=np.uint8)
    for i in range(0, len(msg)):
        msg_matrix[i % 4][i // 4] = ord(msg[i])

    # print_key_matrix_hex(msg_matrix)

    # add round key
    state_matrix = np.bitwise_xor(msg_matrix, scheduled_key[0])

    # 9 rounds
    for i in range(1, 10):
        state_matrix = AES_encrypt_round(state_matrix, scheduled_key[i])

    # last round
    # substitute bytes
    for i in range(0, len(state_matrix)):
        for j in range(0, len(state_matrix[i])):
            state_matrix[i][j] = Sbox[state_matrix[i][j]]

    # shift rows, shift ith row i times
    for i in range(0, len(state_matrix)):
        state_matrix[i] = np.roll(state_matrix[i], -i)

    # add round key
    state_matrix = np.bitwise_xor(state_matrix, scheduled_key[10])

    return matrix_to_string(state_matrix)


def aes_encrypt_msg(msg, scheduled_key, initializing_vector):
    # part the msg in 16 byte chunks
    msg_blocks = split_string_into_blocks(msg)
    do_proper_padding(msg_blocks)

    # print(msg_blocks)

    # first_block is a 16 byte string, comprising of 128 bit '0's, but the character doesn't matter that much
    first_block = [chr(0) * BLOCK_LENGTH_IN_BYTES]
    msg_blocks = first_block + msg_blocks

    xor_block = initializing_vector

    encrypted_msg_blocks = []
    for i in range(0, len(msg_blocks)):
        xor_block = aes_encrypt_block(scheduled_key, bitwise_xor_string(msg_blocks[i], xor_block))
        encrypted_msg_blocks.append(xor_block)

    # join the encrypted blocks
    encrypted_msg = ""
    for i in range(0, len(encrypted_msg_blocks)):
        encrypted_msg += encrypted_msg_blocks[i]
    
    return encrypted_msg

def aes_encrypt(msg, key, initializing_vector):
    return aes_encrypt_msg(msg, schedule_key(make_key(key)), initializing_vector)

# decryption codes
def AES_decrypt_round(state_matrix, key_matrix):
    # inverse shift rows, shift ith row i times
    for i in range(0, len(state_matrix)):
        state_matrix[i] = np.roll(state_matrix[i], i)

    # inverse substitute bytes
    for i in range(0, len(state_matrix)):
        for j in range(0, len(state_matrix[i])):
            state_matrix[i][j] = Sbox_inv[state_matrix[i][j]]

    # add round key
    state_matrix = np.bitwise_xor(state_matrix, key_matrix)

    # inverse mix columns
    state_matrix = mix_columns(state_matrix, inv=True)

    return state_matrix

def aes_decrypt_block(scheduled_key, msg):
    # # convert msg to 4X4 numpy matrix
    msg_matrix = np.zeros((4, 4), dtype=np.uint8)
    for i in range(0, len(msg)):
        msg_matrix[i % 4][i // 4] = ord(msg[i])

    # add round key
    state_matrix = np.bitwise_xor(msg_matrix, scheduled_key[10])

    # 9 rounds
    for i in range(9, 0, -1):
        state_matrix = AES_decrypt_round(state_matrix, scheduled_key[i])

    # last round
    # inverse shift rows, shift ith row i times
    for i in range(0, len(state_matrix)):
        state_matrix[i] = np.roll(state_matrix[i], i)

    # inverse substitute bytes
    for i in range(0, len(state_matrix)):
        for j in range(0, len(state_matrix[i])):
            state_matrix[i][j] = Sbox_inv[state_matrix[i][j]]

    # add round key
    state_matrix = np.bitwise_xor(state_matrix, scheduled_key[0])

    return matrix_to_string(state_matrix)

def aes_decrypt_msg(msg, scheduled_key):
    # part the msg in 16 bytes chunks
    msg_blocks = split_string_into_blocks(msg)

    decrypted_msg_blocks = []
    for i in range(1, len(msg_blocks)):
        decrypted_msg_blocks.append(bitwise_xor_string(aes_decrypt_block(scheduled_key, msg_blocks[i]), msg_blocks[i - 1]))

    decrypted_msg_blocks = remove_proper_padding(decrypted_msg_blocks)
    # print(decrypted_msg_blocks)
    # join the encrypted blocks
    decrypted_msg = ""
    for i in range(0, len(decrypted_msg_blocks)):
        decrypted_msg += decrypted_msg_blocks[i]

    return decrypted_msg

def aes_decrypt(msg, key):
    return aes_decrypt_msg(msg, schedule_key(make_key(key)))

def make_key(key):
    if len(key) == 16:
        return key
    elif len(key) > 16:
        return key[:16]
    else:
        return key + 'X' * (16 - len(key))

def print_string_in_hex(string):
    print("[ ", end="")
    for i in range(0, len(string)):
        print(hex(ord(string[i])), end=" ")
    print("]")


def convert_number_key_to_string(number_key):
    binary_key = bin(number_key)[2:]  # Remove the '0b' prefix from the binary representation
    string_key = ""

    # iterate from the end of the string to the beginning in steps of 8
    for i in range(len(binary_key) - 8, -8, -8):
        # if the number of bits left is less than 8, then take the remaining bits
        if i < 0:
            string_key += chr(int(binary_key[:i + 8], 2))
        else:
            string_key += chr(int(binary_key[i:i + 8], 2))

    return string_key[::-1]


def demonstrate():

    # dealing with key
    # key = "Thats my Kung Fu"
    print("Key: ")
    print("In ASCII: ", end="")
    key = input()

    key = make_key(key)
    print("In HEX: ", end="")
    print_string_in_hex(key)
    print()


    print("Plain Text:")
    print("In ASCII: ", end="")
    msg = input()

    print("In HEX: ", end="")
    print_string_in_hex(msg)
    print()

    # 16 byte string
    initializing_vector = "Thats my Kung Fu"

    start = time.time()
    scheduled_key = schedule_key(key)
    key_schedule_time = time.time() - start

    start = time.time()
    encrypted_string = aes_encrypt_msg(msg, scheduled_key, initializing_vector)
    encryption_time = time.time() - start

    # now printing the encrypted string
    print("Ciphered Text:")
    print("In ASCII: ", end="")
    print(encrypted_string.encode('ascii', 'replace'))
    print("In HEX: ", end="")
    print_string_in_hex(encrypted_string)
    print()

    start = time.time()
    decrypted_string = aes_decrypt_msg(encrypted_string, scheduled_key)
    decryption_time = time.time() - start

    # now printing the decrypted string
    print("Deciphered Text:")
    print("In ASCII: ", end="")
    print(decrypted_string)
    print("In HEX: ", end="")
    print_string_in_hex(decrypted_string)
    print()


    print("Execution Time Details:")
    print("Key Schedule Time: ", key_schedule_time * 1000, "ms")
    print("Encryption Time: ", encryption_time * 1000, "ms")
    print("Decryption Time: ", decryption_time * 1000, "ms")


Rcon.append(1)
for i in range(1, 10):
    if Rcon[i - 1] < 0x80:
        Rcon.append(2 * Rcon[i - 1])
    else:
        Rcon.append((2 * Rcon[i - 1]) ^ 0x11b)


if __name__ == "__main__":
    # print(convert_number_key_to_string(0x41424344))
    demonstrate()

# encrypted_matrix = encrypt_AES(key, msg)

# print(type(encrypted_matrix))
# print("Encypted matrix:")
# print_key_matrix_hex(encrypted_matrix)

# encrypted_string = matrix_to_string(encrypted_matrix)
# print(matrix_to_string(encrypted_matrix))

# decrypted_matrix = decrypt_AES(key, encrypted_string)
# print_key_matrix_hex(decrypted_matrix)

# decrypted_string = matrix_to_string(decrypted_matrix)
# print(decrypted_string)
# # print(convert_matrix_to_string(decrypted_matrix))


