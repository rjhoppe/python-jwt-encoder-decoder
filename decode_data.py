import pickle
import os.path
from jwt import JWT, jwk_from_dict

jwt = JWT()
path_val = ''

def open_key(path_val):
  path = f'./{path_val}'
  check_file = os.path.isfile(path)
  print(path)
  if check_file is True:
    key_file = open('pub-key', 'rb')
    public_key = pickle.load(key_file)
    return public_key
  else:
    raise Exception('Key file not present. Make sure key file is in directory or re-run encode file.')

def open_token(path_val):
  path = f'./{path_val}'
  check_file = os.path.isfile(path)
  if check_file is True:
    token_file = open('token', 'rb')
    token = pickle.load(token_file)
    return token
  else:
    raise Exception('Token file not present. Make sure token file is in directory or re-run encode file.')

def decode(token: str, key: dict) -> str: 
  jwk = jwk_from_dict(key)
  return jwt.decode(token, jwk)

public_key = open_key(path_val='pub-key')
token = open_token(path_val='token')
payload = decode(token, public_key)
print(payload['fact'])