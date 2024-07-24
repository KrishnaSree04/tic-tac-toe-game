import math
from fractions import Fraction
print("(Use log,frac for logarithmic and Fraction operations)")
def calculator(m,n):
    x=input("Enter mode of Calculation:")
    match x:
        case '+':
            print(m+n)
        case '-':
            print((m-n))
        case '*':
            print(m*n)
        case '/':
            print(m/n)
        case '%':
            print(m%n)
        case 'log':
            print(math.log(m,n))
        case 'frac':
            print(Fraction(m,n))
        case 'exp':
            print(m**n)
     
m=int(input())
n=int(input())
calculator(m,n)