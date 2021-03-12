import random
import string

key = ""
stt = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ."
taille = len(stt)
for i in range(100):
    rd = random.randint(0, taille-1)
    print(rd, "taille", taille)
    key += stt[rd]

print(key)