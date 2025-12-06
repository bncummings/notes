from typing import List

def productExceptSelf(nums: List[int]) -> List[int]:
        products = [1] * len(nums)
        prefix_product = 1
        suffix_product = 1

        for i in range(len(nums)):
            products[i] *= prefix_product
            products[len(nums) - 1 - i] *= suffix_product

            prefix_product *= nums[i]
            suffix_product *= nums[len(nums) - 1 - i]

        return products


print(productExceptSelf([1,2,3,4])) 
