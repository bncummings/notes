package divideAndConquer

/**
 * Definition for a QuadTree node.
 *
 */
class Node(var `val`: Boolean, var isLeaf: Boolean) {
         var topLeft: Node? = null
         var topRight: Node? = null
         var bottomLeft: Node? = null
         var bottomRight: Node? = null
}

fun construct(grid: Array<IntArray>): Node? {
    //assume the grid is square
    val dimension = grid.size

    //base case: single cell
    if(dimension == 1) return Node(`val` = grid.first().first() == 1, isLeaf = true)

    // split the grid into quadrants assume that the size is a power of 2
    val topLeft: Array<IntArray> = grid.take(dimension/2).map{(it.take(dimension/2)).toIntArray()}.toTypedArray()
    val topRight = grid.take(dimension/2).map{(it.drop(dimension/2)).toIntArray()}.toTypedArray()
    val bottomLeft = grid.drop(dimension/2).map{(it.take(dimension/2)).toIntArray()}.toTypedArray()
    val bottomRight = grid.drop(dimension/2).map{(it.drop(dimension/2)).toIntArray()}.toTypedArray()

    // call construct on each quadrant
    val subtrees: List<Node> = listOf(topLeft, topRight, bottomLeft, bottomRight).map{
        construct(it)!!
    }

    //if all of them are the same and leaf nodes then we can summarize it with a leaf node
    return if( subtrees.all { it.isLeaf && it.`val` == subtrees.first().`val` }){
        Node(subtrees.first().`val`, true)
    } else {
        val result = Node(`val` = false, isLeaf = false)
        result.topLeft = subtrees[0]
        result.topRight = subtrees[1]
        result.bottomLeft = subtrees[2]
        result.bottomRight = subtrees[3]

        result
    }
}