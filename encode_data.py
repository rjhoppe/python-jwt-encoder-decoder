import requests
import pickle
import uuid
import random
import os.path

from jwcrypto.jwt import JWK
from jwt import JWT, jwk_from_dict

jwt = JWT()
fact = ''
unique_id = str(uuid.uuid4())

def get_fact() -> str:
  r = requests.get("https://cat-fact.herokuapp.com/facts")
  data = r.json()
  rand_int = random.randint(0, 4)
  fact = data[rand_int]['text']
  return fact

def generate_keys() -> object:
  jwk = JWK.generate(kty="RSA", size=2048, alg="RS256", use="sig", kid="420")
  return jwk.export_private(as_dict=True), jwk.export_public(as_dict=True)

def encode(data: object, key):
  jwk = jwk_from_dict(key)
  return jwt.encode(data, jwk, alg="RS256", optional_headers={"type": "JWT"})

def check_encode_output():
  check_token = os.path.isfile('./token')
  check_key = os.path.isfile('./pub-key')
  if check_token is not True or check_key is not True:
    raise Exception('Failed to generate required token and pub-key files')

fact = get_fact()

# Change exp parameter to a future looking UNIX timestamp
if __name__ == "__main__":
  data = {
    "sub": unique_id, 
    "name": "Rick Hoppe", 
    "admin": True, 
    "device": "Rick\'s Computer",
    "exp": 1701401165, 
    "fact": fact,
  }

private_key, public_key = generate_keys()
token = encode(data, private_key)

token_file = open('token', 'wb')
pickle.dump(token, token_file)
token_file.close()

key_file = open('pub-key', 'wb')
pickle.dump(public_key, key_file)
key_file.close()

check_encode_output()