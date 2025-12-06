package binarySearchTrees
import kotlin.math.abs

fun getMinimumDifference(root: TreeNode?): Int {
    var minDistance = Int.MAX_VALUE
    var prev: TreeNode? = null
    //traverse the tree in order. The only possible candidates are pairs of consecutive nodes (in order)

    fun inOrder(node: TreeNode?) {
        //base case: null node
        if(node == null) return

        //keep going left until you can't anymore.
        inOrder(node.left)

        //compare the distances
        if(prev != null) {
            val distance = abs((prev!!.`val` - node.`val`))
            minDistance = minOf(distance, minDistance)
        }

        //finally traverse the right hand side of the sub-tree
        prev = node
        inOrder(node.right)
    }

    inOrder(root)
    return minDistance
}