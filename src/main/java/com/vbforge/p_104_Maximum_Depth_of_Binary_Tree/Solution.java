package com.vbforge.p_104_Maximum_Depth_of_Binary_Tree;

public class Solution {

    public static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;
        TreeNode(int val) { this.val = val; }
    }

    public int maxDepth(TreeNode root) {
        if (root == null) return 0;
        return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
    }

    /**
     * ---
     *
     * **The idea in one sentence:** recursively ask — *what's the deeper side, left or right?* — add 1 for the current node, until you hit `null`.
     *
     * ---
     * */

}
