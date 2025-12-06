package dynamicProgramming

fun main() {
    println(
        minimumTotal(
            listOf(listOf(2),listOf(3,4),listOf(6,5,7),listOf(4,1,8,3))
        )
    )
}

fun minimumTotal(triangle: List<List<Int>>): Int {
    val minMap = HashMap<Pair<Int,Int>, Int>()

    fun minimumTotalFromIndex(row:Int, col:Int): Int =
        minMap.getOrPut(Pair(row,col)) {
            // base case
            if(row == triangle.lastIndex) triangle[row][col]

            else triangle[row][col] + minOf(
                minimumTotalFromIndex(row + 1, col),
                minimumTotalFromIndex(row + 1, col + 1),
            )
        }

    return minimumTotalFromIndex(0,0)
}


