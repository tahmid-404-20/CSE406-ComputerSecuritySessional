from BitVector import BitVector

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

AES_modulus = BitVector(bitstring='100011011')

def gf_multiply(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:
            a ^= AES_modulus
        b >>= 1
    return result

def matrix_multiply(matrix1, matrix2):
    rows1, cols1 = len(matrix1), len(matrix1[0])
    rows2, cols2 = len(matrix2), len(matrix2[0])

    if cols1 != rows2:
        raise ValueError("Number of columns in the first matrix must be equal to the number of rows in the second matrix")

    result = [[BitVector(intVal=0, size=8) for _ in range(cols2)] for _ in range(rows1)]

    for i in range(rows1):
        for j in range(cols2):
            for k in range(cols1):
                result[i][j] ^= BitVector(intVal=gf_multiply(matrix1[i][k].intValue(), matrix2[k][j].intValue()), size=8)

    return result

# Given matrix
input_matrix = [
    [BitVector(hexstring="63"), BitVector(hexstring="eb"), BitVector(hexstring="9f"), BitVector(hexstring="a0")],
    [BitVector(hexstring="2f"), BitVector(hexstring="93"), BitVector(hexstring="92"), BitVector(hexstring="c0")],
    [BitVector(hexstring="af"), BitVector(hexstring="c7"), BitVector(hexstring="ab"), BitVector(hexstring="30")],
    [BitVector(hexstring="a2"), BitVector(hexstring="20"), BitVector(hexstring="cb"), BitVector(hexstring="2b")]
]

# Multiply the given matrix with the Mixer matrix
result_matrix = matrix_multiply(input_matrix, Mixer)

# Print the result
print("Result of multiplying the matrices:")
for row in result_matrix:
    print([bv.get_bitvector_in_hex() for bv in row])
