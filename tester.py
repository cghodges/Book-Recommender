zeroRatings = [0]*5

ratings = {'tim':zeroRatings.copy(), 'kim':zeroRatings.copy()}


print(ratings['tim'])

ratings['kim'][0] = 7

print(ratings['tim'])

print(ratings['kim'])