package com.vbforge.p_155_Min_Stack;


import java.util.Stack;

public class Solution {

    private final Stack<Integer> mainStack;
    private final Stack<Integer> minStack;

    public Solution() {
        this.mainStack = new Stack<>();
        this.minStack = new Stack<>();
    }

    public void push(int val) {
        mainStack.push(val);
        if (minStack.isEmpty() || val <= minStack.peek()) {
            minStack.push(val);
        } else {
            minStack.push(minStack.peek());
        }
    }

    public void pop() {
        mainStack.pop();
        minStack.pop();
    }

    public int top() {
        return mainStack.peek();
    }

    public int getMin() {
        return minStack.peek();
    }

    /**
     * Your Solution object will be instantiated and called as such:
     * Solution obj = new Solution();
     * obj.push(val);
     * obj.pop();
     * int param_3 = obj.top();
     * int param_4 = obj.getMin();
     */

    public static void main(String[] args) {
        Solution solution = new Solution();
        solution.push(-2);
        solution.push(0);
        solution.push(-3);
        System.out.println(solution.getMin()); // -3
        solution.pop();
        System.out.println(solution.top());    // 0
        System.out.println(solution.getMin()); // -2
    }

}
