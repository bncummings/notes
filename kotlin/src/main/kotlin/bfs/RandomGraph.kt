package bfs

import java.util.Random

fun main() {
 println(RandomGraph())
}

class RandomGraph(
    maxDegree: Int = 8
) {
    val adjacencyMatrix: List<List<Int>>

    init{
        val rng = Random()
        val upperTriangular = List(maxDegree) { i ->
            List(maxDegree) { j ->
                if(j < i) 0 else  rng.nextInt(2)
            }
        }

        adjacencyMatrix = symmetriseUpperTriangularMatrix(upperTriangular)
    }

    /**
     * Given an upper triangular matrix,
     * return the unique corresponding matrix which is symmetric about the leading diagonal
     *
     * Constraint: upperTriangular matrix must be square
     */
    private fun symmetriseUpperTriangularMatrix(upperTriangular: List<List<Int>>): List<List<Int>> {

        /* quick, weak assertion that the matrix is square */
        require(upperTriangular.size == upperTriangular.first().size)

        val tempMatrix = upperTriangular.map(Collection<Int>::toMutableList).toMutableList()

        for (i in 0 until tempMatrix.size) {
            for (j in i until  tempMatrix.size) {
                tempMatrix[j][i] = tempMatrix[i][j]
            }
        }

        return tempMatrix
    }

    override fun toString(): String {
        if (adjacencyMatrix.isEmpty()) return "[]"

        val colWidths = adjacencyMatrix[0].indices.map { col ->
            adjacencyMatrix.maxOf { row -> row[col].toString().length }
        }

        return adjacencyMatrix.joinToString("\n") { row ->
            row.mapIndexed { i, v ->
                v.toString().padStart(colWidths[i])
            }.joinToString("  ", prefix = "[ ", postfix = " ]")
        }
    }
}
