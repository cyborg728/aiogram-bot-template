# https://gist.github.com/fabiolimace/6db9747f83b02e62db55afed8461ee5b

from uuid import UUID
from time import time_ns
from random import randint

TOTAL_BITS = 128
VERSION_BITS = 4
VARIANT_BITS: int = 2

# Binary digits before the binary point
SEC_BITS = 38

# Binary digits after the binary point
SUBSEC_BITS_S = 0
SUBSEC_BITS_MS = 10
SUBSEC_BITS_US = 20
SUBSEC_BITS_NS = 30
SUBSEC_BITS_DEFAULT = SUBSEC_BITS_NS

# Decimal digits after the decimal point
SUBSEC_DECIMAL_DIGITS_S = 0  # 0
SUBSEC_DECIMAL_DIGITS_MS = 3  # 0.999
SUBSEC_DECIMAL_DIGITS_US = 6  # 0.999999
SUBSEC_DECIMAL_DIGITS_NS = 9  # 0.999999999
SUBSEC_DECIMAL_DIGITS_DEFAULT = SUBSEC_DECIMAL_DIGITS_NS

SLICE_MASK_0 = 0xFFFFFFFFFFFF00000000000000000000
SLICE_MASK_1 = 0x0000000000000FFF0000000000000000
SLICE_MASK_2 = 0x00000000000000003FFFFFFFFFFFFFFF


def uuid7(
    t=None,
    subsec_bits=SUBSEC_BITS_DEFAULT,
    subsec_decimal_digits=SUBSEC_DECIMAL_DIGITS_DEFAULT,
):
    if t is None:
        t = time_ns()

    i = get_integer_part(t)
    f = get_fractional_part(t, subsec_decimal_digits)

    sec = i
    subsec = round(f * (2**subsec_bits))

    node_bits = (
        TOTAL_BITS - VERSION_BITS - VARIANT_BITS - SEC_BITS - subsec_bits
    )

    uuid_sec = sec << (subsec_bits + node_bits)
    uuid_subsec = subsec << node_bits
    uuid_node = randint(0, (2**node_bits))

    uuid_int = uuid_sec | uuid_subsec | uuid_node  # 122 bits
    uuid_int = __add_version__(uuid_int)  # 128 bits

    return UUID(int=uuid_int)


def uuid7_s(t=None):
    return uuid7(t, SUBSEC_BITS_S, SUBSEC_DECIMAL_DIGITS_S)


def uuid7_ms(t=None):
    return uuid7(t, SUBSEC_BITS_MS, SUBSEC_DECIMAL_DIGITS_MS)


def uuid7_us(t=None):
    return uuid7(t, SUBSEC_BITS_US, SUBSEC_DECIMAL_DIGITS_US)


def uuid7_ns(t=None):
    return uuid7(t, SUBSEC_BITS_NS, SUBSEC_DECIMAL_DIGITS_NS)


# noinspection PyRedundantParentheses
def __add_version__(uuid_int):
    slice_mask_0 = SLICE_MASK_0 >> (VERSION_BITS + VARIANT_BITS)
    slice_mask_1 = SLICE_MASK_1 >> (VARIANT_BITS)
    slice_mask_2 = SLICE_MASK_2

    slice_0 = (uuid_int & slice_mask_0) << (VERSION_BITS + VARIANT_BITS)
    slice_1 = (uuid_int & slice_mask_1) << (VARIANT_BITS)
    slice_2 = uuid_int & slice_mask_2

    uuid_output = slice_0 | slice_1 | slice_2
    uuid_output = (
        uuid_output & 0xFFFFFFFFFFFF0FFF3FFFFFFFFFFFFFFF
    )  # clear version
    uuid_output = (
        uuid_output | 0x00000000000070008000000000000000
    )  # apply version

    return uuid_output


# noinspection PyRedundantParentheses
def __rem_version__(uuid_int):
    slice_0 = (uuid_int & SLICE_MASK_0) >> (VERSION_BITS + VARIANT_BITS)
    slice_1 = (uuid_int & SLICE_MASK_1) >> (VARIANT_BITS)
    slice_2 = uuid_int & SLICE_MASK_2

    uuid_output = slice_0 | slice_1 | slice_2

    return uuid_output


def get_integer_part(t):
    subsec_decimal_digits_python = 9
    subsec_decimal_divisor = 10**subsec_decimal_digits_python
    return int(t / subsec_decimal_divisor)


def get_fractional_part(
    t, subsec_decimal_digits=SUBSEC_DECIMAL_DIGITS_DEFAULT
):
    subsec_decimal_digits_python = 9
    subsec_decimal_divisor = 10**subsec_decimal_digits_python
    return round(
        (t % subsec_decimal_divisor) / subsec_decimal_divisor,
        subsec_decimal_digits,
    )


def extract_sec(uuid):
    uuid_int = __rem_version__(uuid.int)
    uuid_sec = uuid_int >> (
        TOTAL_BITS - VERSION_BITS - VARIANT_BITS - SEC_BITS
    )
    return uuid_sec


# noinspection PyRedundantParentheses
def extract_subsec(
    uuid,
    subsec_bits=SUBSEC_BITS_DEFAULT,
    subsec_decimal_digits=SUBSEC_DECIMAL_DIGITS_DEFAULT,
):
    uuid_int = __rem_version__(uuid.int)
    node_bits = (
        TOTAL_BITS - VERSION_BITS - VARIANT_BITS - SEC_BITS - subsec_bits
    )
    uuid_subsec = (uuid_int >> node_bits) & ((1 << (subsec_bits)) - 1)
    return round(uuid_subsec / (2**subsec_bits), subsec_decimal_digits)


# def list():

#     print("UUIDv7                               sec in       sec out      subsec in    subsec out")

#     for i in range(10):
#         t = time_ns()
#         u = uuid7(t)
#         i = get_integer_part(t)
#         f = get_fractional_part(t)
#         sec = extract_sec(u)
#         subsec = extract_subsec(u)
#         print(u, str(i).ljust(12), str(sec).ljust(12),
#               str(f).ljust(12), str(subsec).ljust(12))

# list()
