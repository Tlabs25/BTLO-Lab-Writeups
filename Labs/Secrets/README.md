# BTLO — Secrets

## Overview

These are the steps and tools used to complete this exercise.

### Tools Used

* [JWT.io](https://jwt.io/) — Decode and inspect the JWT
* Python — Crack the weak JWT signing secret

---

## 1. Decode the JWT

Looking at the token provided, we can identify it as a **JSON Web Token (JWT)**.

I used **JWT.io** to decode the token.

### Header

```json
{
  "typ": "JWT",
  "alg": "HS256"
}
```

### Payload

```json
{
  "flag": "BTL{_4_Eyes}",
  "iat": 90000000,
  "name": "GreatExp",
  "admin": true
}
```

The header shows that the token uses the **HS256** signing algorithm.

The payload also contains an `admin` claim set to `true`, indicating that this is currently a high-privilege token.

---

# Questions

## Question 1: Can you identify the name of the token?

The token type can be found in the JWT header under the `typ` field.

```json
"typ": "JWT"
```

**Answer:** `JWT`

---

## Question 2: What is the structure of this token?

JWTs follow the structure:

```text
HEADER.PAYLOAD.SIGNATURE
```

The three sections are separated by periods (`.`).

* **Header** — Contains information such as the token type and signing algorithm.
* **Payload** — Contains the claims/data stored in the token.
* **Signature** — Used to verify that the token has not been modified.

---

## Question 3: What is the hint you found from this token?

The hint is found directly in the payload:

```json
"flag": "BTL{_4_Eyes}"
```

**Answer:** `_4_Eyes`

---

## Question 4: What is the secret?

The JWT uses **HS256**, meaning the signature is generated using a shared secret.

The secret is not directly visible when decoding the JWT, so it needs to be recovered by testing possible secrets against the existing signature.

I used a Python script named `cracker.py` to perform this process.

### What the script does

1. Takes the JWT.
2. Splits it into the header, payload, and signature.
3. Generates possible 4-character secrets based on the challenge requirements.
4. Calculates the HMAC-SHA256 signature using each candidate secret.
5. Base64URL-encodes the calculated signature.
6. Compares it against the original JWT signature.
7. Prints the matching secret when one is found.

Conceptually:

```text
Candidate Secret
       ↓
HMAC-SHA256
       ↓
Base64URL Encode
       ↓
Compare with JWT Signature
       ↓
Match = Correct Secret
```

The recovered secret can then be used to create a new valid JWT signature.

---

## Question 5: Can you generate a new verified signature ticket with a low privilege?

The challenge asks for a **low-privilege** ticket.

The original payload contains:

```json
"admin": true
```

This needs to be changed to:

```json
"admin": false
```

After modifying the payload, the original signature is no longer valid because the contents of the token have changed.

Using the secret recovered in Question 4, a new **HS256 signature** can be generated for the modified payload.

I used **JWT.io** to:

1. Change `admin` from `true` to `false`.
2. Enter the recovered signing secret.
3. Generate the new signature.
4. Verify that the resulting JWT is valid.

The resulting token is the required **low-privilege ticket**.

---

## Key Takeaway

This exercise demonstrates how a weak JWT signing secret can compromise the integrity of a token.

Even though the JWT payload can be decoded without the secret, the signature normally prevents an attacker from modifying the payload and creating a valid token.

If the signing secret is weak enough to recover, an attacker can:

```text
Recover Secret
      ↓
Modify JWT Claims
      ↓
Generate New Signature
      ↓
Create Valid Modified JWT
```

In this case, the attacker can change the `admin` claim from `true` to `false` and generate a valid low-privilege token.
