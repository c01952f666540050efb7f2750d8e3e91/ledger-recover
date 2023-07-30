# IMPORT
from phrase import generate_recovery_phrase
from ledger_recover import *

# Let's generate our recovery phrase with that code
test_phrase = generate_recovery_phrase()

# Here is a print of what we've created!
for x in test_phrase.keys():
    print(f"{x} // {test_phrase[x]}")

"""
Now that we have a recovery phrase to perform the recover process on, we can proceed accordingly!

I want to show later, that you don't even have to do it with a recovery phrase, as the process of shamir's secret sharing,
(and consequently pedersen verifiable secret sharing) can be performed on some arbitrary set of data, to imbue it with
the properties we desire.

Remember, in this process we have vastly oversimplified the process.

"""

# Let's take the string of the phrase because it's easier. Remember in real life it's the entropy not the phrase
test_string = test_phrase['phrase']
print(test_string)

# let's convert it to an int (number or integer)
test_int = string_to_int(test_string)
print(test_int)

# Now we can 'imbue' this number with the properties we want
test_shares = create_shares(test_int, 3, 2)
print()
for x in test_shares:
    print(f"{x}\n")

test_out = reconstruct_secret(test_shares)
print(test_out)