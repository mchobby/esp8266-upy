from stat import linear_regression

# Example data
x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 4, 5]

m, b = linear_regression(x, y)

# Equation y = m * x + b
print( "Slope (m): %s" % m ) # Coef de la droite 
print( "Intercept (b): %s" % b ) # ordonée
print( "Equation: y = %s * x + %s" % (m,b) )