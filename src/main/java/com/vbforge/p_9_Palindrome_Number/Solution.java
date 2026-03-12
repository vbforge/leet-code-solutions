package com.vbforge.p_9_Palindrome_Number;

public class Solution {

    public boolean isPalindrome(int x) {

        // negative numbers are not palindrome
        if (x < 0) return false;

        // numbers ending with 0 (but not 0 itself)
        if (x != 0 && x % 10 == 0) return false;

        int reversed = 0;

        while (x > reversed) {
            int digit = x % 10;
            reversed = reversed * 10 + digit;
            x /= 10;
        }

        return x == reversed || x == reversed / 10;
    }

}
