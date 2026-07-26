import oqs

KEM_ALGORITHM = "ML-KEM-768"

print("=" * 50)
print("SecureDrone PQC Handshake Demo")
print("=" * 50)

# Drone generates a key pair
with oqs.KeyEncapsulation(KEM_ALGORITHM) as drone:

    drone_public_key = drone.generate_keypair()

    print("\nDrone Public Key Generated")
    print("Public Key Length:", len(drone_public_key), "bytes")

    # Ground Control Station
    with oqs.KeyEncapsulation(KEM_ALGORITHM) as gcs:

        ciphertext, gcs_shared_secret = gcs.encap_secret(drone_public_key)

        print("\nCiphertext Generated")
        print("Ciphertext Length:", len(ciphertext), "bytes")

    # Drone recovers the shared secret
    drone_shared_secret = drone.decap_secret(ciphertext)

print("\nChecking Shared Secret...")

if drone_shared_secret == gcs_shared_secret:
    print("\nSUCCESS ✅")
    print("Both parties generated the SAME shared secret.")
else:
    print("\nFAILED ❌")