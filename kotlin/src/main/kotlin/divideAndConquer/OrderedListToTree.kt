package divideAndConquer
import kotlin.math.ceil

class TreeNode(var `val`: Int) {
    var left: TreeNode? = null
    var right: TreeNode? = null
}

fun sortedArrayToBST(nums: IntArray): TreeNode? {
    if(nums.isEmpty()) return null
    if(nums.size == 1) return TreeNode(nums[0])

    val middleIndex: Int = nums.size / 2
    val currentNode = TreeNode(nums[middleIndex])
    currentNode.left = sortedArrayToBST(nums.take(middleIndex).toIntArray())
    currentNode.right = sortedArrayToBST(nums.drop(middleIndex + 1).toIntArray())
    return currentNode

}
