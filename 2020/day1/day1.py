
def findyear(year, data):
  result = []
  for start, a in enumerate(data):
    for b in data[start + 1:]:
      if a + b == year:
        result.append(a)
        result.append(b)
        return result
  return result

if __name__ == '__main__':
  with open('input') as f:
    data = f.read().split('\n')
  data = [int(x) for x in data if x]
  x, y = findyear(2020, data)
  print(x*y)

  for i, a in enumerate(data):
    remainder = 2020 - a
    result = findyear(remainder, data[i + 1:])
    if len(result) == 2:
      print(a * result[0] * result[1])
      break
