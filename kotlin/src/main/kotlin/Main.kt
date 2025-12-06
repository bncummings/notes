
private const val MAX = 10

data class ListOfTwo(var left: Int, val right:Int) {
}

fun main() {
    val numbers = ListOfTwo.default()

    println(ListOfTwo.MAX)
}

//fun negateLeftNumber(numbers: Pair<Int, Int>) {
//    numbers.left *= -1;
//}
//
//fun negate(x:Int) {
//    x = -x
//}
