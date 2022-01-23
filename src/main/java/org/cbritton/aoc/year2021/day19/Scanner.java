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
    int[] originPosition = null;
    int[][] rotationMatrix = null;

    Scanner(String name, int[][] beacons) {
        this.name = name;
        this.beacons = beacons;
    }

    boolean isOriented() {
        return null != this.rotationMatrix;
    }

    Scanner rotate(int[][] rotationMatrix) {

        List<int[]> rotatedBeacons = new ArrayList<>();
        for (int[] beacon : this.beacons) {
            rotatedBeacons.add(rotateBeacon(rotationMatrix, beacon));
        }
        Scanner rotated_scanner = new Scanner(this.name, rotatedBeacons.toArray(new int[][] { }));
        rotated_scanner.rotationMatrix = rotationMatrix;
        rotated_scanner.originPosition = this.originPosition;
        return rotated_scanner;
    }

    int[] translate(int[] beacon) {
        return new int[] { beacon[0] + this.originPosition[0], beacon[1] + this.originPosition[1],
                beacon[2] + this.originPosition[2] };
    }

    int find(int[] beacon, int[][] beacons) {

        for (int i = 0; i < beacons.length; ++i) {
            if ((beacons[i][0] == beacon[0]) && (beacons[i][1] == beacon[1]) && (beacons[i][2] == beacon[2])) {
                return i;
            }
        }
        return -1;
    }

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

    private int compareSegmentToOther(Scanner other, int match_count, int[] b1Self, int[] b2Self) {

        for (int[] b1Other : other.beacons) {
            for (int[] b2Other : other.beacons) {
                if (b1Other == b2Other) {
                    continue;
                }
                if (((b1Self[0] - b2Self[0]) - (b1Other[0] - b2Other[0])) == 0 && ((b1Self[1] - b2Self[1]) - (b1Other[1] - b2Other[1])) == 0 && ((b1Self[2] - b2Self[2]) - (b1Other[2] - b2Other[2])) == 0) {
                    if (++match_count >= MINIMUM_COMMON_BEACONS) {
                        other.originPosition = new int[] { this.originPosition[0] - (b1Other[0] - b1Self[0]),
                                this.originPosition[1] - (b1Other[1] - b1Self[1]),
                                this.originPosition[2] - (b1Other[2] - b1Self[2]) };
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
