""" base58 encoding / decoding functions """
alphabet = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
base_count = len(alphabet)

def to_base128(s):#Creates number from string
	total = 0
	for c in s:
		total <<= 7
		total += ord(c)
	return total

def from_base128(i):#Creates string from number
	r=[]
	while i>0:
		r=[chr(i%128)]+r
		i>>=7
	return ''.join(r)

def encode(num):
	""" Returns num in a base58-encoded string """
	encode = ''
	
	if (num < 0):
		return ''
	
	while (num >= base_count):	
		mod = num % base_count
		encode = alphabet[mod] + encode
		num = num / base_count

	if (num):
		encode = alphabet[num] + encode

	return encode

def decode(s):
	""" Decodes the base58-encoded string s into an integer """
	decoded = 0
	multi = 1
	s = s[::-1]
	for char in s:
		decoded += multi * alphabet.index(char)
		multi = multi * base_count
		
	return decoded

if __name__ == '__main__':
	import unittest

	class Base58Tests(unittest.TestCase):

		def test_alphabet_length(self):
			self.assertEqual(58, len(alphabet))

		def test_encode_10002343_returns_Tgmc(self):
			result = encode(10002343)
			self.assertEqual('Tgmc', result)

		def test_decode_Tgmc_returns_10002343(self):
			decoded = decode('Tgmc')
			self.assertEqual(10002343, decoded)

		def test_encode_1000_returns_if(self):
			result = encode(1000)
			self.assertEqual('if', result)

		def test_decode_if_returns_1000(self):
			decoded = decode('if')
			self.assertEqual(1000, decoded)

		def test_encode_zero_returns_empty_string(self):
			self.assertEqual('', encode(0))

		def test_encode_negative_number_returns_empty_string(self):
			self.assertEqual('', encode(-100))

	unittest.main()