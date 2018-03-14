with open('nlist', 'w') as f:
    for i in range(1,10000000,10000):
        f.write(str(i) +'\n')
