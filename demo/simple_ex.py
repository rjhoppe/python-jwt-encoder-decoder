from jwcrypto.jwt import JWK
from jwt import JWT, jwk_from_dict

# Almost like a client
jwt = JWT()

def generate_keys():
  # kty = key type
  jwk = JWK.generate(kty="RSA", size=2048, alg="RS256", use="sig", kid="420")
  return jwk.export_private(as_dict=True), jwk.export_public(as_dict=True)

def encode(data, key):
  # Similarity between jwk and jwt is very confusing to the eyes...
  jwk = jwk_from_dict(key)
  return jwt.encode(data, jwk, alg="RS256", optional_headers={"type": "JWT"})

def decode(token, key):
  jwk = jwk_from_dict(key)
  return jwt.decode(token, jwk)

if __name__ == "__main__":
  data = {"sub": "1234567890", "name": "John Doe", "admin": True, "iat": 1516239022}
  # Could also define an expiration for token in data using exp 
  # Example: {"exp": 100} -> 100 milliseconds

  private_key, public_key = generate_keys()
  token = encode(data, private_key)
  payload = decode(token, public_key)
  print(public_key)
  print(token)
  print(payload)