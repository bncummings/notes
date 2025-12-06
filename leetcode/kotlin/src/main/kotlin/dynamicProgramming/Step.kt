package dynamicProgramming

/**
 * 1d dynamic programming with memoization
 */
val soluitionMap = HashMap<Int, Int>()

fun climbStairs(n: Int): Int {
    if(n == 0) return 1
    if(n == 1) return 1
    if(soluitionMap.containsKey(n)) return soluitionMap[n]!!

    val solution = climbStairs(n - 1) + climbStairs(n - 2)
    soluitionMap.put(n, solution)

    return solution
}