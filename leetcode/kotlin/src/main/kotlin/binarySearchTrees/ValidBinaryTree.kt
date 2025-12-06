package binarySearchTrees

/**
 * Test cases don't allow for duplicate elements.
 * They also test against the max and min Int values, so I had to use longs.
 */
fun isValidBST(root: TreeNode?): Boolean {

    //every node has an associated max and min that it must lie in
    fun isValidNode(node: TreeNode?, min: Long, max: Long): Boolean {
        //base case
        if(node == null) return true
        //check val in range
        if(node.`val` >= max || node.`val` <= min) return false
        //check children against respective ranges
        return isValidNode(node.left, min, node.`val`.toLong())
                && isValidNode(node.right, node.`val`.toLong(), max)

    }

    return isValidNode(root, Long.MIN_VALUE , Long.MAX_VALUE)
}