package org.cbritton.aoc.year2021.day19;

import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import static org.cbritton.TimeUtil.elapsedTime;
import static org.cbritton.aoc.year2021.day19.Rotation.ROTATIONS;

/**
 * Process pairs of scanners by rotating and translating them in 3D space to determine which ones overlap. The
 * following definitions are used in the algorithm below.
 * <dl>
 *     <dt>beacon</dt><dd>a point in 3D Euclidean space.</dd>
 *     <dt>oriented</dt><dd>a scanner is oriented when it is rotated to the same orientation as scanner 0.</dd>
 *     <dt>overlap</dt><dd>two scanners overlap if they share at least 12 common beacons.</dd>
 *     <dt>rotate</dt><dd>to apply the dot product of one of 24 90&deg; rotation matrices to a beacon. To rotate a
 *     scanner is to rotate all of its beacons.</dd>
 *     <dt>scanner</dt><dd>a collection of beacons.</dd>
 *     <dt>translate</dt><dd>to determine the origin of a scanner (once it has been oriented) relative to scanner 0.
 *     </dd>
 * </dl>
 * The simulator processes pairs of scanners. The first scanner in a pair is always oriented. That is, its
 * position and orientation in 3D space relative to scanner 0 is known. The second scanner of the pair is not
 * oriented. The simulator attempts to determine if the scanners overlap. For each of the 24 possible rotations of
 * the unoriented scanner:
 * <ul>
 *     <li>Rotate the unoriented scanner.</li>
 *     <li>Calculate the vector that is the distance between all permutations of pairs of beacons for the
 *     oriented scanner.</li>
 *     <li>Calculate the vector that is the distance between all permutations of pairs of beacons for the
 *     unoriented scanner.</li>
 *     <li>If there are 12 or more vectors from the unoriented scanner that equal vectors in the oriented scanner,
 *     stop. The unoriented scanner overlaps the oriented scanner.</li>
 *     <li>Otherwise, rotate the unoriented scanner with the next rotation matrix and repeat the process.</li>
 *     <li>If no overlap can be found with any of the 24 rotations, skip the current unoriented scanner and go to
 *     the next unoriented scanner. The skipped scanner will be processed with next oriented scanner.</li>
 * </ul>
 * The process is complete when there are no remaining unoriented scanners to process.
 */
class Simulator {

    private static final Simulator instance = new Simulator();

    private Map<String, Scanner> scanners = null;

    public static Simulator getInstance() {
        return instance;
    }

    /**
     * Determines if there is a rotation of the unoriented scanner that will result in at least 12 common distance
     * vectors between beacon pairs.
     *
     * @param orientedScanner   the oriented scanner to compare
     * @param unorientedScanner the unoriented scanner to compare
     */
    private void findOverlaps(Scanner orientedScanner, Scanner unorientedScanner) {

        for (int[][] rotationMatrix : ROTATIONS) {
            Scanner rotatedScanner = unorientedScanner.rotate(rotationMatrix);
            if (orientedScanner.overlapsWith(rotatedScanner)) {
                unorientedScanner.origin = rotatedScanner.origin;
                unorientedScanner.rotationMatrix = rotationMatrix;
                unorientedScanner.beacons = rotatedScanner.beacons;
                break;
            }
        }
        return;
    }

    /**
     * Indicates if there are any unoriented scanners remaining.
     *
     * @return <code>true</code> if there are no unoriented scanners. <code>false</code> if there are one or more
     * unoriented scanners remaining.
     */
    private boolean done() {

        for (Scanner scanner : this.scanners.values()) {
            if (!scanner.isOriented()) {
                return false;
            }
        }
        return true;
    }

    /**
     * Compares oriented and unoriented scanners by rotating the unoriented scanners and looking for overlaps.
     */
    private void findOverlappingBeacons() {

        while (!done()) {
            for (String s1Name : this.scanners.keySet()) {
                for (String s2Name : this.scanners.keySet()) {
                    if (s1Name.equals(s2Name)) {
                        continue;
                    }
                    Scanner s1 = this.scanners.get(s1Name);
                    Scanner s2 = this.scanners.get(s2Name);
                    if (!s1.isOriented() && s2.isOriented()) {
                        Scanner tmp = s1;
                        s1 = s2;
                        s2 = tmp;
                    }
                    if (s1.isOriented() && !s2.isOriented()) {
                        findOverlaps(s1, s2);
                    }
                }
            }
        }
        return;
    }

    /**
     * Determines the total number of beacons after orienting all scanners to construct the full map of beacons.
     */
    private void findTotalBeaconCount() {

        long startTimeMillis = System.currentTimeMillis();
        findOverlappingBeacons();

        Set<int[]> beacons = new HashSet<>();
        for (String scannerName : this.scanners.keySet()) {
            for (int[] beacon : this.scanners.get(scannerName).beacons) {
                int[] translatedBeacon = this.scanners.get(scannerName).translate(beacon);
                if (!this.scanners.get(scannerName).contains(translatedBeacon, beacons.toArray(new int[][] { }))) {
                    beacons.add(translatedBeacon);
                }
            }
        }
        long endTimeMillis = System.currentTimeMillis();
        System.out.println("\nPart 1:");
        System.out.println("    Beacon count: " + beacons.size());
        System.out.println("    Elapsed time: " + elapsedTime(startTimeMillis, endTimeMillis));

        return;
    }

    /**
     * Runs the simulation with the specified data.
     *
     * @param scanners the scanners to map
     */
    void run(Map<String, Scanner> scanners) {

        this.scanners = scanners;
        findTotalBeaconCount();
        return;
    }
}
