def luhn(input):
    ints = list(map(lambda x: int(x), list(input)))
    ints.reverse()
    for i in range(len(ints)):
        ints[i] = (ints[i] * (i%2+1))
    return sum(map(lambda x: x//10 + x % 10, ints))%10 == 0
        
def digit_finder(input):
    for i in range(10):
        temp = input.replace("X", str(i))
        if luhn(temp): return i
    
def list_solver (cards):
    result = ""
    for card in cards:
        result += str(digit_finder(card))
    return result

cards = []
with open("cards.txt", "r") as f:
    for line in f:
        cards.append(line.rstrip())

print(list_solver(cards))
