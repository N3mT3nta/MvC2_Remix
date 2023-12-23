a = ['1', '2', '3']

b = '123'
for pos,item in enumerate(a):
    print(pos, item)


'''str = '06AB0046820B0046803F023C00688244'
file = open('MvC2.iso', 'rb')
print(str in file.read().hex())
'''

'''
file = open('LICENSE', 'rb')
file_hex = file.read().hex()
file_hex = file_hex.replace('a0b0', 'aaaa')
print(file_hex)
new_file = open('bin\\DUMMY', 'wb')
new_file.write(bytes.fromhex(file_hex))
'''



'''
file = open('bin\\DUMMY', 'rwb')
file_hex = file.read().hex()
file_hex = file_hex.replace('000', '111')
file = open('bin\\DUMMY', 'wb')
file.write(bytes.fromhex(file_hex))
file.close()
'''