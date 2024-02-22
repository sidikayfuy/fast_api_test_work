def calculate_median(list_values):
    values = [float(x) for x in list_values.split(',')]
    values.sort()
    n = len(values)
    if n % 2 == 0:
        median = (values[n // 2 - 1] + values[n // 2]) / 2
    else:
        median = values[n // 2]
    return median