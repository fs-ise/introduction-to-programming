provision = 0

while True:
    vs = float(input('Versicherungssumme: '))
    if vs!=0:
        provision = provision + 50 + vs * 0.01
    else:
        break

print('Provision:', provision)
