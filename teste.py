'''import re

# string de entrada
string = "03051107212"

# quebra a string, mas inclui strings vazias
lista = re.split("(\S{3})", string)



# remove strings vazias, deixa apenas o que interessa
final = list(filter(None, lista))

print(final)'''

teste = input("CPF: ") # 12345678900
