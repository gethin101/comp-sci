from dataclasses import dataclass
@dataclass

class Product: 
    name:str
    price:float
    category:str
    stock_count:0

laptop = Product("Laptop", 132.99 , "Electronics" , 20)
food = Product("Meal", 4.99 , "Consumable" , 90)
PC = Product("Desktop", 650.00 , "Electronics" , 10)


#=================================================

print()
print("========== Products: ============")
print()
print("Product 1:")
print (f'Product name: {laptop.name}')
print (f'Product price: {laptop.price}')
print (f'Product category: {laptop.category}')
print (f'Product stock count: {laptop.stock_count}')
print()

print("Product 2:")
print (f'Product name: {food.name}')
print (f'Product price: {food.price}')
print (f'Product category: {food.category}')
print (f'Product stock count: {food.stock_count}')
print()

print("Product 3:")
print (f'Product name: {PC.name}')
print (f'Product price: {PC.price}')
print (f'Product category: {PC.category}')
print (f'Product stock count: {PC.stock_count}')
print()

#==================================================

print("====== Modifications: =======")
laptop.stock_count= 19
print (f'Laptop stock count changed to: {laptop.stock_count}')
print("==================================")
print()

