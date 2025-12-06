package binarySearchTrees

fun kthSmallest(root: TreeNode?, k: Int): Int {
    var counter = 0
    var res: Int? = null

    //traverse from left to right, returning the kth element
    fun inOrder(current: TreeNode?) {
        //base case
        if(current == null || res != null) return

        inOrder(current.left)

        //count how many nodes we've visited so far
        counter++
        if(counter == k) {
            res = current.`val`
        }

        inOrder(current.right)
    }

    inOrder(root)
    return res!!
}
