# You have a list of ‘powers’ e.g. [4,3,3,6,8]. 
# You want to find the maximum total power you can use. 
# If you use power value n, you can’t use power value n-1 or n+1. 
# In the example I gave, the max would be 3+3+6+8=20

def powers(powers: list[int]) -> int:
    # we need to keep totals of the case where we keep or skip a number
    # if we take a number, we can always take that number.
    # go through the values in a sorted fashion
    # if we run into an adjacent pair
        # if we take this one then we skipped the previous one

    
