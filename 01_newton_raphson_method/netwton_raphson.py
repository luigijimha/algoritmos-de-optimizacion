from sympy import symbols, sympify

"""
adds right padding to number for printing table
@param {double} number    number to add left padding
@return {String}          number with left padding
"""
def rpad(number):
    message = str(number)
    return message + ' ' * (25 - len(message))

x = symbols('x')
padding_spacing = 15

xNew = float(input("input starting value: "))
max_iterations = int(input("input max iterations: "))

expression = input("input function: ")
function = sympify(expression)

error = 10

print("\nxi                        f(x)                      f'(x)                     x(i+1)                    error                    ")

while (abs(error) > 0.00000001) and (max_iterations != 0):
    # set x value
    xOld = xNew
    # calculate f(x)
    func = function.subs(x, xOld)
    # calculate f'(x)
    dfunc = function.diff(x).subs(x, xOld)
    # get x(i+1)
    xNew = xOld - func / dfunc
    # calculate error
    error = xOld - xNew

    print(rpad(xOld) + " "
          + rpad(func) + " "
          + rpad(dfunc) + " "
          + rpad(xNew) + " "
          + rpad(error))

    max_iterations -= 1

if max_iterations != 0:
    print("Root is located at", xNew)
else:
    print("Maximum iterations reached")
