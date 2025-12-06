package dynamicProgramming

val solutionMap = HashMap<IntArray, Int>()
fun rob(nums: IntArray): Int =
    solutionMap.getOrPut(nums) {
        when (nums.size){
            0 -> 0
            1 -> nums[0]
            2 -> Integer.max(nums[0], nums[1])
            else -> Integer.max(
                nums[0] + rob(nums.drop(2).toIntArray()),
                nums[1] + rob(nums.drop(3).toIntArray()),
            )
        }
    }
