import toml

def init():
  data = {
    'title': 'Project name',
    'info': {
      'username': 'username',
      'password': 'password',
    }
  }
  with open('pyproject.toml', 'w') as toml_file:
    toml.dump(data, toml_file)