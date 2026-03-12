package com.vbforge.p_1_Two_Sum;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.*;

class SolutionTest {

    @Test
    void basicExample() {
        assertArrayEquals(new int[]{0, 1}, Solution.twoSum(new int[]{2, 7, 11, 15}, 9));
    }

    @Test
    void middleElements() {
        assertArrayEquals(new int[]{1, 2}, Solution.twoSum(new int[]{3, 2, 4}, 6));
    }

    @Test
    void sameElementTwice() {
        assertArrayEquals(new int[]{0, 1}, Solution.twoSum(new int[]{3, 3}, 6));
    }

    @ParameterizedTest
    @MethodSource("provideTestCases")
    void parameterized(int[] nums, int target, int[] expected) {
        assertArrayEquals(expected, Solution.twoSum(nums, target));
    }

    static Stream<Arguments> provideTestCases() {
        return Stream.of(
                Arguments.of(new int[]{2, 7, 11, 15}, 9,  new int[]{0, 1}),
                Arguments.of(new int[]{3, 2, 4},      6,  new int[]{1, 2}),
                Arguments.of(new int[]{3, 3},          6,  new int[]{0, 1})
        );
    }
}