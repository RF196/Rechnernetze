import struct

# <ID><RechenOperation><N><z1><z1>...<zN>
#  I   10s             B   i
# Rechenoperation = Summe Produkt Minimum Maximum

var = struct.pack('<I10sBii', 1, b'Summe', 2, 1, 2)
(id, operation, anzahl) = struct.unpack('<I10sB', var[:15])
(op1, op2) = struct.unpack('ii', var[15:])
operation_decoded = operation.decode('utf-8')
print(id, operation_decoded, anzahl, op1, op2)
print("i" * 4)
