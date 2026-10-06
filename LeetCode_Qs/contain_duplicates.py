def contains_duplicate(nums):
    # Your solution here
    assert isinstance(nums, list)
    if len(nums) == 0:
        return False


    # indexes= range(len(nums))
    # for i in indexes:
    #     for j in indexes:
    #         if i == j:
    #             pass
    #         elif nums[i] == nums[j]:
    #             return True
    # return False

    # for i in range(len(nums)):
    #     for j in range(i+1, len(nums)):
    #         if nums[i] == nums[j]:
    #             return True
            
    # return False

    seen = set()
    for num in nums:
        if num in seen:
            return True
        else:
            seen.add(num)

    return False

                
    
#[]

if __name__ == "__main__":
    print(contains_duplicate([1, 2, 3, 1]))  # True
    print(contains_duplicate([1, 2, 3, 4]))  # False