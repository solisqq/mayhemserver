def powWlasna(value, potega):
    result = value
    for i in range(1,potega):
        result = result*value
    return result

print(powWlasna(2,3))
