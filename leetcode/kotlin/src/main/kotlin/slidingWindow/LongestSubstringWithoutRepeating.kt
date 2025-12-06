package slidingWindow

fun main(args: Array<String>) {
    println("Hello World!")

    // Try adding program arguments via Run/Debug configuration.
    // Learn more about running applications: https://www.jetbrains.com/help/idea/running-applications.html.
    println(lengthOfLongestSubstring("abcabcbb"))
}

fun lengthOfLongestSubstring(s: String): Int {
    var left = 0
    var right = 0
    val characterSet:HashSet<Char> = hashSetOf()

    var candidate:List<Char> = listOf()
    val current:MutableList<Char> = mutableListOf()

    //if we reach the last index we should just return
    while(right < s.length) {
        //if s[right] is not in the character set
        // then add s[right] to the set and increment right
        if(!characterSet.contains(s[right])) {
            characterSet.add(s[right])
            current.add(s[right])
            right++
            // if it's a longer length than the current candidate then replace it
            if(current.size > candidate.size) {
                candidate = current.toList()
            }
            System.out.println(candidate)
        } else {
            current.removeFirst()
            characterSet.remove(s[left])
            left++
        }
    }

    return candidate.size
}