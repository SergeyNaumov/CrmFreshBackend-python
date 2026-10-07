import hashlib
import random

try:
  import crypt as _crypt
except Exception:
  _crypt = None

# Символы соли DES (как в crypt(3)) — для ENCRYPT-совместимого формата.
_DES_SALT = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def _sha256(value):
  return hashlib.sha256(str(value).encode('utf-8')).hexdigest()


def verify_password(plain, stored):
  """Проверяет пароль против любого известного формата хранения.

  Поддержаны: plaintext, sha2-256 (64), md5 (32) и crypt (DES/ENCRYPT —
  13 символов, а также современные $1$/$5$/$6$). MySQL 8 удалил ENCRYPT(),
  поэтому проверку старых записей делаем на стороне Python.
  """
  if plain is None or stored is None:
    return False
  plain = str(plain)
  stored = str(stored).strip()
  if not stored:
    return False
  if stored == plain:
    return True
  low = stored.lower()
  if len(stored) == 64 and low == _sha256(plain):
    return True
  if len(stored) == 32 and low == hashlib.md5(plain.encode('utf-8')).hexdigest():
    return True
  if _crypt is not None:
    try:
      if _crypt.crypt(plain, stored) == stored:
        return True
    except Exception:
      pass
  return False


def hash_password(plain, method=None):
  """Хэширует пароль для хранения.

  mysql_encrypt (legacy) → DES/ENCRYPT-совместимый crypt(3), если доступен
  модуль crypt; иначе sha2-256. mysql_sha2 → sha2-256.
  """
  plain = '' if plain is None else str(plain)
  if method != 'mysql_sha2' and _crypt is not None:
    try:
      salt = ''.join(random.choice(_DES_SALT) for _ in range(2))
      out = _crypt.crypt(plain, salt)
      if out and out not in ('*0', '*1'):
        return out
    except Exception:
      pass
  return _sha256(plain)
