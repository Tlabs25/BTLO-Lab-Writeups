import base64
import hashlib
import hmac
import itertools
import string
import time


# =========================
# Configuration
# =========================

JWT = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiQlRMe180X0V5ZXN9IiwiaWF0Ijo5MDAwMDAwMCwibmFtZSI6IkdyZWF0RXhwIiwiYWRtaW4iOnRydWV9.jbkZHll_W17BOALT95JQ17glHBj9nY-oWhT1uiahtv8"


# =========================
# JWT / HMAC functions
# =========================

def base64url_encode(data):
    """Encode bytes using JWT-compatible Base64URL."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def check_secret(secret, message, target_signature):
    """Check whether a candidate secret produces the JWT signature."""

    digest = hmac.new(
        secret.encode(),
        message,
        hashlib.sha256
    ).digest()

    calculated_signature = base64url_encode(digest)

    return hmac.compare_digest(
        calculated_signature,
        target_signature
    )


# =========================
# Parse JWT
# =========================

try:
    header, payload, target_signature = JWT.split(".")

except ValueError:
    print("[-] Invalid JWT.")
    print("[-] Make sure it has the format:")
    print("    HEADER.PAYLOAD.SIGNATURE")
    exit()


# The data that HS256 signs
message = f"{header}.{payload}".encode()


# =========================
# Candidate character sets
# =========================

lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
special = "!@#$%^&*"
digits = string.digits


# =========================
# Start search
# =========================

print("[*] JWT loaded.")
print("[*] Algorithm: HS256")
print("[*] Searching for a 4-character secret...")
print("[*] Pattern: lowercase + uppercase + special + digit")
print()


start_time = time.time()
attempts = 0
found = False


for candidate in itertools.product(
    lowercase,
    uppercase,
    special,
    digits
):

    secret = "".join(candidate)
    attempts += 1

    if check_secret(
        secret,
        message,
        target_signature
    ):

        elapsed = time.time() - start_time

        print("[+] SECRET FOUND!")
        print(f"[+] Secret: {secret}")
        print(f"[+] Attempts: {attempts}")
        print(f"[+] Time: {elapsed:.2f} seconds")

        found = True
        break


# =========================
# Search completed
# =========================

if not found:

    elapsed = time.time() - start_time

    print("[-] Secret was not found.")
    print(f"[-] Attempts: {attempts}")
    print(f"[-] Time: {elapsed:.2f} seconds")
