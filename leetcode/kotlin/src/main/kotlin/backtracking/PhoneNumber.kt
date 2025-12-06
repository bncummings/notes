package backtracking

val letterMap: Map<Int, List<String>> = mapOf(
    2 to listOf("a", "b", "c"),
    3 to listOf("d", "e", "f"),
    4 to listOf("g", "h", "i"),
    5 to listOf("j", "k", "l"),
    6 to listOf("m", "n", "o"),
    7 to listOf("p", "q", "r", "s"),
    8 to listOf("t", "u", "v"),
    9 to listOf("w", "x", "y", "z")
)

fun letterCombinations(digits: String): List<String> {
    if(digits.isEmpty()) return emptyList()

    val firstLetters: List<String> = letterMap[digits[0].digitToInt()]!!

    //special case when there is only one digit left
    if(digits.length == 1) return firstLetters

    //get all the letters from firstDigit, and for each one add
    return firstLetters.flatMap{ prefix ->
        letterCombinations(digits.drop(1)).map{
                suffix -> prefix + suffix
        }
    }
}