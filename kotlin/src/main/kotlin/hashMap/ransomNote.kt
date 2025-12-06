import java.util.HashMap
fun main() {

}
fun canConstruct(ransomNote: String, magazine: String): Boolean {
    val letterMap = HashMap<Char, Int>()
    //for each letter in the magazine store it in the map
    magazine.forEach{
        // letterMap[it] = letterMap.getOrPut(it) {0} + 1
        letterMap.merge(it, 1, Int::plus)
    }
    //for each letter in the message decrement its corresponding value
    ransomNote.forEach{
        if( !letterMap.contains(it) || letterMap[it]!! <= 0) {
            return false
        }
        letterMap.merge(it, -1, Int::plus)
    }

    return true
}