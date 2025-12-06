package bfs

import java.util.Random

class RandomTree(
    maxDepth: Int = 6,
    maxValue: Int = 100,
    maxNumberOfChildren: Int = 8
) {
    val root: Node

    init {
        val depth = Random().nextInt(maxDepth)
        fun generateNode(currentDepth: Int): Node {
            val value = Random().nextInt(maxValue)
            if(currentDepth == 0) return Node(value)

            /* generate a random number of children */
            val numberOfChildren = Random().nextInt(maxNumberOfChildren)

            return Node(
                value,
                MutableList(numberOfChildren) {
                    generateNode(currentDepth - 1)
                }
            )
        }
        root = generateNode(depth)
    }
}
