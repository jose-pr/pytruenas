from pytruenas.utils import text



for letter in text.range('a', 'f'):
    print(letter)

for letter in text.range('1', '10'):
    print(letter)


for t in text.expand("test[1-15:x].[text[c-h]]"):
    print(t)

pass