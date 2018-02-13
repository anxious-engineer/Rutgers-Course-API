import boto3

funcs = boto3.client('lambda').list_functions().get("Functions")
# print(type(funcs))
# print(len(funcs))
for func in funcs:
    print(func.get('FunctionName'))
