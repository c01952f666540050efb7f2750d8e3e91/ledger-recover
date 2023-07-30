# import binascii
import base64
import random
import sympy
import functools

def string_to_int(s):
    return int.from_bytes(base64.b64encode(s.encode()), 'big')

def int_to_string(n):
    return base64.b64decode(n.to_bytes((n.bit_length() + 7) // 8, 'big')).decode()

def create_shares(secret_int, num_shares, threshold):
    # Int already converted
    coefficients = [secret_int] + [random.randint(0, secret_int) for _ in range(threshold - 1)]
    polynomial = sympy.Poly(coefficients, sympy.symbols('x'))
    shares = [(i, int(polynomial.subs('x', i))) for i in range(1, num_shares + 1)]
    return shares

# def reconstruct_secret(shares):
#     x_values, y_values = zip(*shares)
#     secret_int = functools.reduce(lambda a, b: a + b, [y_values[i] * functools.reduce(lambda a, b: a * b, [(x_values[j] / (x_values[j] - x_values[i])) for j in range(len(x_values)) if i != j]) for i in range(len(x_values))])
#     return int_to_string(int(secret_int))
import decimal

def reconstruct_secret(shares):
    decimal.getcontext().prec = 50  # Set the precision to 50
    x_values, y_values = zip(*shares)
    x_values = [decimal.Decimal(x) for x in x_values]
    y_values = [decimal.Decimal(y) for y in y_values]
    secret_int = sum(
        y_values[i] * functools.reduce(
            lambda a, b: a * b,
            [
                x_values[j] / (x_values[i] - x_values[j])
                for j in range(len(x_values)) if i != j
            ]
        )
        for i in range(len(x_values))
    )
    print(secret_int)
    exit()
    return int_to_string(int(secret_int))