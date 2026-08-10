These are the steps and tools used to complete this exercise

Looking at the token given, its a JWT so first we decode it. I used jwt.io

This is what I got:

{
  "typ": "JWT",
  "alg": "HS256"
}

{
  "flag": "BTL{_4_Eyes}",
  "iat": 90000000,
  "name": "GreatExp",
  "admin": true
}

We also see that ther is no proper signature verification, so we will need to find that later

Let's start working through the questions

Question 1: Can you identify the name of the token?
Can be found in the header identified by "typ"

Question 2: What is the structure of this token?
All JWTs follow the same structure header.payload.signature

Question 3: What is the hint you found from this token?
Found directly in the payload

Question 4: What is the secret?
We will need to crack the JWT to find this. I will be using a python script name cracker.py
From the hint we know that the secret will be 4 characters long

This is what the code will do

Takes the JWT.
Splits it into header/payload/signature.
Generate possible secrets
Calculates HMAC-SHA256 for each candidate.
Compares the result against the JWT's signature.
Prints the matching secret.

After the secret is pulled we can move to question 5

Question 5: Can you generate a new verified signature ticket with a low privilege?
It wants a low privilege ticket so admin:true needs to become admin:false. Afterwards use the secret found in question 4 then go back to jwt.io  and you got the key!
