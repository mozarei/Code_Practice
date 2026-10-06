
from collections import Counter 

    
def anagram1(t, s):
    if len(t) != len(s):
        return False

    return Counter(t) == Counter(s)

class AnagramChecker:
    def anagram2(self,t,s):
        if len(t) != len(s):
            return False 

        counts ={}

        for letter in t:
            if letter in counts:
                counts[letter] += 1
            else:
                counts[letter] = 1

            # counts[letter] = counts.get(letter, 0) + 1 

        for letter in s:
            if letter not in counts:
                return False

            if counts[letter] == 0:
                return False

            counts[letter] -= 1

        return True
            





if __name__ == "__main__":
    # print(anagram2("listen", "silents"))
    checker = AnagramChecker
    print(checker.anagram2("listen", "silent"))
    # test_cases = [
    #     ("listen", "silent", True),
    #     ("hello", "world", False),
    #     ("cat", "cats", False),
    #     ("aab", "abb", False),
    #     ("aab", "aba", True),
    #     ("", "", True),
    #     ("a", "a", True),
    # ]

    # passed = 0
    # for t, s, expected in test_cases:
    #     try:
    #         result = anagram(t, s)
    #         if result is expected:
    #             passed += 1
    #             print(f"PASS: anagram({t!r}, {s!r}) -> {result}")
    #         else:
    #             print(
    #                 f"FAIL: anagram({t!r}, {s!r}) "
    #                 f"expected {expected}, got {result!r}"
    #             )
    #     except Exception as error:
    #         print(
    #             f"FAIL: anagram({t!r}, {s!r}) "
    #             f"raised {type(error).__name__}: {error}"
    #         )

    # print(f"\n{passed}/{len(test_cases)} tests passed.")
