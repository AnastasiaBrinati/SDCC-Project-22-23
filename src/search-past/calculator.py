def minimum(nums):
  min = nums[0]
  for n in nums:
    if(n<min):
      min = n
  return min

def maximum(nums):
  max = nums[0]
  for n in nums:
    if(n>max):
      max = n
  return max

def avg(nums):
  sum = 0
  for n in nums:
    #if(n<min):
    sum += n
  return sum/len(nums)