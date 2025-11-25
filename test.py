#####------------------------------------------------------------Test File for List inside Function Calling Scenerios,same scenerios will be for others data type (tuple,dict,set)------------------------------------------------------------

# ------------------------------------------------------------Function Definition Scenerios------------------------------------------------------------
# def testing_function(*items): #-->first scenerio in whcih we are unpacking items
#     for item in items:
#         print(item)
#     return "This is a test function."


# def testing_function(*items): #-->second scenerio in whcih list is passed as it is and unpacking is done along with the list itself returning
#     for item in items:
#         print(item)
#     return "This is a test function."


# def testing_function(items): #-->third scenerio in whcih list is passed as it is and  returning the items separately
#     for item in items:
#         print(item)
#     return "This is a test function."


# def testing_function(items): #-->third scenerio in whcih list is passed as it is and  returning the items separately
#     for item in items:
#         print(item)
#     return "This is a test function."


# def testing_function(item1=None,item2=None,item3=None): #-->fourth scenerio in whcih items are passed separately is passed as it is and  returning the items separately,it is similar to third scenerio,first scenerio
#     for item in [item1,item2,item3]:
#         print(item)    
#     #OR can be used separately values
#     #print(f"Item 1: {item1}, Item 2: {item2}, Item 3: {item3}")    
#     return "This is a test function."

# def testing_function(items): #-->fifth scenerio in whcih list is passed as it is and  returning the new item added inside function but will reflect outside as well
#     changes_done_insdie_function_will_reflect_outside = items #-->reference assignment    
#     for item in items:
#         print(item)
#     changes_done_insdie_function_will_reflect_outside.append({"name": "Soda", "price": 100, "quantity": 1})
#     return "This is a test function."

# def testing_function(items=[]): #-->6th scenerio in whcih list is passed as it is and  returning the new item added inside function but will reflect outside as well
#     changes_done_insdie_function_will_reflect_outside = items #-->default mutable argument
#     for item in items:
#         print(item)
#     changes_done_insdie_function_will_reflect_outside.append({"name": "Soda", "price": 100, "quantity": 1})
#     return "This is a test function."

# def testing_function(items): #-->7th scenerio in whcih list is passed as it is and  returning the new item added inside function but will not reflect outside
#     changes_done_insdie_function_will_not_reflect_outside = items.copy() or [] #-->shallow copy
#     for item in items:
#         print(item)
#     changes_done_insdie_function_will_not_reflect_outside.append({"name": "Soda", "price": 100, "quantity": 1})
#     return "This is a test function."

# def testing_function(items=None): #-->8th scenerio in whcih list is passed as it is and  returning the new item added inside function but will not reflect outside for every call of the funciton but will create new list for every call
#     changes_done_insdie_function_will_not_reflect_outside = items.copy() or [] #-->shallow copy
#     for item in items:
#         print(item)
#     changes_done_insdie_function_will_not_reflect_outside.append({"name": "Soda", "price": 100, "quantity": 1})
#     return "This is a test function."



# ------------------------------------------------------------Function Calling Scenerios------------------------------------------------------------


# items = [
#     {"name": "Burger", "price": 250, "quantity": 2},
#     {"name": "Pasta", "price": 300, "quantity": 1},
#     {"name": "Fries", "price": 120, "quantity": 3}
# ]


#result = testing_function(*items)-->first scenerio in whcih we are unpacking items,mean each item will be passed as separately
#print(result)
# {'name': 'Burger', 'price': 250, 'quantity': 2}
# {'name': 'Pasta', 'price': 300, 'quantity': 1}
# {'name': 'Fries', 'price': 120, 'quantity': 3}

# result = testing_function(items)-->second scenerio in whcih list is passed as it is and unpacking is done along with the list itself returning
#print(result)
# [{'name': 'Burger', 'price': 250, 'quantity': 2}, {'name': 'Pasta', 'price': 300, 'quantity': 1}, {'name': 'Fries', 'price': 120, 'quantity': 3}]

# result = testing_function(items) #-->third scenerio in whcih list is passed as it is and  returning the items separately
#print(result)
# {'name': 'Burger', 'price': 250, 'quantity': 2}
# {'name': 'Pasta', 'price': 300, 'quantity': 1}
# {'name': 'Fries', 'price': 120, 'quantity': 3}

# result = testing_function(item1=items[0],item2=items[1],item3=items[2]) #-->fourth scenerio in whcih items are passed separately is passed as it is and  returning the items separately,it is similar to third scenerio,first scenerio
# {'name': 'Burger', 'price': 250, 'quantity': 2}
# {'name': 'Pasta', 'price': 300, 'quantity': 1}
# {'name': 'Fries', 'price': 120, 'quantity': 3}
# print(result)

# result = testing_function(items)#-->fifth scenerio in whcih list is passed as it is and  returning the new item added inside function but will  reflect outside as well
# print(result)

# result = testing_function(items)#-->sixth scenerio in whcih list is passed as it is and  returning the new item added inside function but will not reflect outside
# print(result)


# result = testing_function(items) #-->7th scenerio in whcih list is passed as it is and  returning the new item added inside function but will not reflect outside
# print(result)


# result = testing_function(items) #-->8th scenerio in whcih list is passed as it is and  returning the new item added inside function but will not reflect outside for every call of the funciton but will create new list for every call
# print(result)