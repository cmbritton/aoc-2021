package org.cbritton.aoc.year2021.day19;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

import static org.cbritton.aoc.year2021.day19.Rotation.rotateBeacon;

/**
 * A collection of beacons.
 */
class Scanner {

    static final int MINIMUM_COMMON_BEACONS = 12;

    String name = null;
    int[][] beacons = null;
    int[] origin = null;
    int[][] rotationMatrix = null;

    /**
     * Creates a new <code>Scanner</code> to associate a name with a collection of beacons.
     *
     * @param name    the name of the new scanner
     * @param beacons the set of beacons for the scanner
     */
    Scanner(String name, int[][] beacons) {
        this.name = name;
        this.beacons = beacons;
    }

    /**
     * Indicates if this scanner is in the same orientation as scanner 0.
     *
     * @return <code>true</code> if this scanner is in the same orientation as scanner 0. <code>false</code> otherwise.
     */
    boolean isOriented() {
        return null != this.rotationMatrix;
    }

    /**
     * Rotates all beacons for this scanner using the specified rotation matrix. Beacons are rotated to one of 24
     * 90&deg; turns around the x, y, and z axes.
     *
     * @param rotationMatrix the matrix to use to rotate beacons
     * @return a new <code>Scanner</code> whose beacons are now oriented based on the given rotation matrix
     */
    Scanner rotate(int[][] rotationMatrix) {

        List<int[]> rotatedBeacons = new ArrayList<>();
        for (int[] beacon : this.beacons) {
            rotatedBeacons.add(rotateBeacon(rotationMatrix, beacon));
        }
        Scanner rotated_scanner = new Scanner(this.name, rotatedBeacons.toArray(new int[][] { }));
        rotated_scanner.rotationMatrix = rotationMatrix;
        rotated_scanner.origin = this.origin;
        return rotated_scanner;
    }

    /**
     * Creates new coordinates for the specified beacon. The new coordinates are relative to scanner 0.
     *
     * @param beacon the beacon to translate
     * @return new coordinates based on scanner 0 being the origin
     */
    int[] translate(int[] beacon) {
        return new int[] { beacon[0] + this.origin[0], beacon[1] + this.origin[1], beacon[2] + this.origin[2] };
    }

    /**
     * Indicates if the specified beacon is in the specified array of beacons.
     *
     * @param beacon  the target beacon of the search
     * @param beacons the array of beacons to search
     * @return <code>true</code> if the specified array of beacons contains the specified beacon. <code>false</code>
     * otherwise.
     */
    boolean contains(int[] beacon, int[][] beacons) {

        for (int[] b : beacons) {
            if ((b[0] == beacon[0]) && (b[1] == beacon[1]) && (b[2] == beacon[2])) {
                return true;
            }
        }
        return false;
    }

    /**
     * Indicates if the specified scanner overlaps this scanner.
     *
     * @param other the scanner to compare
     * @return <code>true</code> if this scanner overlaps the specified scanner. <code>false</code> if they do not
     * overlap.
     */
    boolean overlapsWith(Scanner other) {

        int match_count = 0;
        for (int[] b1Self : this.beacons) {
            for (int[] b2Self : this.beacons) {
                if (b1Self == b2Self) {
                    continue;
                }
                match_count = compareSegmentToOther(other, match_count, b1Self, b2Self);
                if (match_count >= MINIMUM_COMMON_BEACONS) {
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * Determines how many distance vectors in the specified scanner coincide with the distance vector specified by
     * the <code>b1Self</code> and <code>b2Self</code> beacons.
     *
     * @param other       the scanner whose beacons define the distance vectors to compare
     * @param match_count the current number of distance vectors matched for the <code>other</code> scanner
     * @param b1Self      the first beacon of the target distance vector
     * @param b2Self      the second beacon of the target distance vector
     * @return the number of distance vectors in the <code>other</code> scanner that coincide with the one specified
     * by <code>b1Self</code> and <code>b2Self</code>.
     */
    private int compareSegmentToOther(Scanner other, int match_count, int[] b1Self, int[] b2Self) {

        for (int[] b1Other : other.beacons) {
            for (int[] b2Other : other.beacons) {
                if (b1Other == b2Other) {
                    continue;
                }
                if (((b1Self[0] - b2Self[0]) - (b1Other[0] - b2Other[0])) == 0
                        && ((b1Self[1] - b2Self[1]) - (b1Other[1] - b2Other[1])) == 0
                        && ((b1Self[2] - b2Self[2]) - (b1Other[2] - b2Other[2])) == 0) {
                    if (++match_count >= MINIMUM_COMMON_BEACONS) {
                        other.origin = new int[] {
                                this.origin[0] - (b1Other[0] - b1Self[0]),
                                this.origin[1] - (b1Other[1] - b1Self[1]),
                                this.origin[2] - (b1Other[2] - b1Self[2])
                        };
                        return match_count;
                    }
                }
            }
            if (match_count >= MINIMUM_COMMON_BEACONS) {
                break;
            }
        }
        return match_count;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }

        Scanner scanner = (Scanner) o;

        return Objects.equals(name, scanner.name);
    }

    @Override
    public int hashCode() {
        return name != null ? name.hashCode() : 0;
    }
}
