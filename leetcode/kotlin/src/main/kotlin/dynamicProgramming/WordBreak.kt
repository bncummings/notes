package dynamicProgramming

fun main() {
    println(wordBreak("leetcode", listOf("leet", "code")))
}


val memo: MutableMap<String, Boolean> = mutableMapOf()

fun wordBreak(s: String, wordDict: List<String>): Boolean {
    if(s == "") return true
    // iterate over the string and take the substring up to that point,
    // look it up in the wordDictionary and call wordBreak on the remainder.

    return memo.getOrPut(s) {
        for(i in 1 .. s.length) {
            val prefix = s.substring(0 until i)
            if(prefix in wordDict) {
                val suffix =  s.substring(i until s.length)
                if (wordBreak(suffix, wordDict)) return@getOrPut true
            }
        }
        return@getOrPut false
    }
}