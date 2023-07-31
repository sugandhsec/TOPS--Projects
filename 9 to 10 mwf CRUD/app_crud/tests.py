import random
list1=['a','t','b','-',"+",'7','8','9','6','9']
key=random.choices(list1,k=25)
print(key)
mainkey="".join(key)
print(mainkey)