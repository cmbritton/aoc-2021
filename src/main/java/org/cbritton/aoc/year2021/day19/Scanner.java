package org.cbritton.aoc.year2021.day19;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class Scanner {

    static final int MINIMUM_COMMON_BEACONS = 12;

    static final int[][][] ROTATIONS = new int[][][]{
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
                    { 1, 0, 0 },
                    { 0, 1, 0 },
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

    String name = null;
    int[][] beacons = null;
    int[] originPosition = null;
    int[][] rotationMatrix = null;
    Map<String, int[]> commonIndexes = new HashMap<>();

    Scanner(String name, int[][] beacons) {
        this.name = name;
        this.beacons = beacons;
    }

    private static int[] rotateBeacon(int[][] rotationMatrix, int[] beacon) {

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

    boolean isOriented() {
        return null != this.rotationMatrix;
    }

    Scanner rotate(int[][] rotationMatrix) {

        List<int[]> rotatedBeacons = new ArrayList<>();
        for (int[] beacon : this.beacons) {
            rotatedBeacons.add(rotateBeacon(rotationMatrix, beacon));
        }
        Scanner rotated_scanner = new Scanner(this.name, rotatedBeacons.toArray(new int[][]{ }));
        rotated_scanner.rotationMatrix = rotationMatrix;
        rotated_scanner.originPosition = this.originPosition;
        return rotated_scanner;
    }

    int[] translate(int[] beacon) {
        return new int[]{ beacon[0] + this.originPosition[0],
                beacon[1] + this.originPosition[1],
                beacon[2] + this.originPosition[2]
        };
    }

    int find(int[] beacon, int[][] beacons) {

        for (int i = 0; i < beacons.length; ++i) {
            if ((beacons[i][0] == beacon[0]) && (beacons[i][1] == beacon[1]) && (beacons[i][2] == beacon[2])) {
                return i;
            }
        }
        return -1;
    }

    int computeCommonBeacons(Scanner other) {

        List<Integer> commonIndexesSelf = new ArrayList<>();
        List<Integer> commonIndexesOther = new ArrayList<>();
        for (int[] b1Self : this.beacons) {
            for (int[] b2Self : this.beacons) {
                if (b1Self == b2Self) {
                    continue;
                }
                for (int[] b1Other : other.beacons) {
                    for (int[] b2Other : other.beacons) {
                        if (b1Other == b2Other) {
                            continue;
                        }
                        if (((b1Self[0] - b2Self[0]) - (b1Other[0] - b2Other[0])) == 0 &&
                                ((b1Self[1] - b2Self[1]) - (b1Other[1] - b2Other[1])) == 0 &&
                                ((b1Self[2] - b2Self[2]) - (b1Other[2] - b2Other[2])) == 0) {
                            int idx = find(b1Self, this.beacons);
                            if (!commonIndexesSelf.contains(idx)) {
                                commonIndexesSelf.add(idx);
                            }
                            idx = find(b2Self, this.beacons);
                            if (!commonIndexesSelf.contains(idx)) {
                                commonIndexesSelf.add(idx);
                            }
                            idx = find(b1Other, other.beacons);
                            if (!commonIndexesOther.contains(idx)) {
                                commonIndexesOther.add(idx);
                            }
                            idx = find(b2Other, other.beacons);
                            if (!commonIndexesOther.contains(idx)) {
                                commonIndexesOther.add(idx);
                            }
                            if (commonIndexesSelf.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                                if (commonIndexesOther.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                                    break;
                                }
                            }
                        }
                        if (commonIndexesSelf.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                            if (commonIndexesOther.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                                break;
                            }
                        }
                    }
                    if (commonIndexesSelf.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                        if (commonIndexesOther.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                            break;
                        }
                    }
                }
                if (commonIndexesSelf.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                    if (commonIndexesOther.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                        break;
                    }
                }
            }
        }
        if (commonIndexesSelf.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
            this.commonIndexes.put(other.name, commonIndexesSelf.stream().mapToInt(i -> i).toArray());
        }

        if (commonIndexesOther.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
            other.commonIndexes.put(this.name, commonIndexesOther.stream().mapToInt(i -> i).toArray());
        }

        return commonIndexesSelf.size();
    }
}
