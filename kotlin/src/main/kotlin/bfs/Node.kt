package bfs

data class Node(
    val value: Int,
    val children: MutableList<Node> = mutableListOf()
)
