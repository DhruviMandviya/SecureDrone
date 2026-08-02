from backend.security.keypair import KeyPair

print("=" * 60)
print("Testing Generic KeyPair")
print("=" * 60)

keys = KeyPair()

keys.generate()

print("✓ Key Pair Generated")

print("Public Key Length :", len(keys.public_key), "bytes")
print("Private Key Length:", len(keys.private_key), "bytes")