package org.cbritton.aoc.year2021.day19;

/**
 * Utility class that defines the 24 possible 90&deg; rotations around the x, y, and z axes.
 */
public class Rotation {

    /**
     * The identity (no rotation) vector.
     */
    static final int[][] IDENTITY_MATRIX = new int[][] {
            { 1, 0, 0 },
            { 0, 1, 0 },
            { 0, 0, 1 }
    };

    /**
     * The rotation vectors around the x, y, and z axes in 90&deg; steps.
     */
    static final int[][][] ROTATIONS = new int[][][] {
            IDENTITY_MATRIX,
            {
                    { 1, 0, 0 },
                    { 0, 0, -1 },
                    { 0, 1, 0 },
            },
            {
                    { 1, 0, 0 },
                    { 0, -1, 0 },
                    { 0, 0, -1 }
            },
            {
                    { 1, 0, 0 },
                    { 0, 0, 1 },
                    { 0, -1, 0 }
            },
            {
                    { 0, 0, 1 },
                    { 0, 1, 0 },
                    { -1, 0, 0 }
            },
            {
                    { -1, 0, 0 },
                    { 0, 1, 0 },
                    { 0, 0, -1 }
            },
            {
                    { 0, 0, -1 },
                    { 0, 1, 0 },
                    { 1, 0, 0 }
            },
            {
                    { 0, -1, 0 },
                    { 1, 0, 0 },
                    { 0, 0, 1 }
            },
            {
                    { -1, 0, 0 },
                    { 0, -1, 0 },
                    { 0, 0, 1 }
            },
            {
                    { 0, 1, 0 },
                    { -1, 0, 0 },
                    { 0, 0, 1 }
            },
            {
                    { 0, 0, 1 },
                    { 1, 0, 0 },
                    { 0, 1, 0 }
            },
            {
                    { -1, 0, 0 },
                    { 0, 0, 1 },
                    { 0, 1, 0 }
            },
            {
                    { 0, 0, -1 },
                    { -1, 0, 0 },
                    { 0, 1, 0 }
            },
            {
                    { 0, -1, 0 },
                    { 0, 0, -1 },
                    { 1, 0, 0 }
            },
            {
                    { -1, 0, 0 },
                    { 0, 0, -1 },
                    { 0, -1, 0 }
            },
            {
                    { 0, 1, 0 },
                    { 0, 0, -1 },
                    { -1, 0, 0 }
            },
            {
                    { 0, 0, 1 },
                    { 0, -1, 0 },
                    { 1, 0, 0 }
            },
            {
                    { 0, 0, -1 },
                    { 0, -1, 0 },
                    { -1, 0, 0 }
            },
            {
                    { 0, -1, 0 },
                    { -1, 0, 0 },
                    { 0, 0, -1 }
            },
            {
                    { 0, 1, 0 },
                    { 1, 0, 0 },
                    { 0, 0, -1 }
            },
            {
                    { 0, 0, 1 },
                    { -1, 0, 0 },
                    { 0, -1, 0 }
            },
            {
                    { 0, 0, -1 },
                    { 1, 0, 0 },
                    { 0, -1, 0 }
            },
            {
                    { 0, -1, 0 },
                    { 0, 0, 1 },
                    { -1, 0, 0 }
            },
            {
                    { 0, 1, 0 },
                    { 0, 0, 1 },
                    { 1, 0, 0 }
            }
    };

    /**
     * Rotates the specified beacon (3D coordinates) using the dot product with the specified rotation matrix.
     * @param rotationMatrix the rotation matrix (vector) to translate the specified beacon
     * @param beacon the beacon to rotate
     * @return a new beacon whose coordinates are the dot product of the rotation matrix and the original beacon
     */
    static int[] rotateBeacon(int[][] rotationMatrix, int[] beacon) {

        int[] rotatedBeacon = new int[3];
        for (int i = 0; i < 3; ++i) {
            int result = 0;
            for (int j = 0; j < 3; ++j) {
                result += rotationMatrix[i][j] * beacon[j];
            }
            rotatedBeacon[i] = result;
        }
        return rotatedBeacon;
    }
}
