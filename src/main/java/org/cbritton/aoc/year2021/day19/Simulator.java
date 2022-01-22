package org.cbritton.aoc.year2021.day19;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.util.concurrent.TimeUnit;

class Simulator {

    private final Map<String, Scanner> scanners = new HashMap<>();

    private void initData() {

        try (BufferedReader file = new BufferedReader(new FileReader("data/day19.data"))) {
            List<int[]> beacons = null;
            String scannerName = null;
            String line;
            while ((line = file.readLine()) != null) {
                if (line.startsWith("---")) {
                    if (null != beacons) {
                        scanners.put(scannerName, new Scanner(scannerName, beacons.toArray(new int[][]{ })));
                    }
                    beacons = new ArrayList<>();
                    scannerName = "scanner " + line.split(" ")[2];
                    continue;
                }
                if (!line.isBlank()) {
                    String[] values = line.split(",");
                    assert beacons != null;
                    beacons.add(new int[]{ Integer.parseInt(values[0]), Integer.parseInt(values[1]),
                            Integer.parseInt(values[2]) });
                }
            }
            assert beacons != null;
            scanners.put(scannerName, new Scanner(scannerName, beacons.toArray(new int[][]{ })));
            Scanner scanner = scanners.get("scanner 0");
            scanner.originPosition = new int[]{ 0, 0, 0 };
            scanner.rotationMatrix = new int[][]{
                    { 1, 0, 0 },
                    { 0, 1, 0 },
                    { 0, 0, 1 }
            };
        } catch (IOException e) {
            System.err.println("Error. msg = " + e.getMessage());
        }
        return;
    }

    private void findOverlaps(Scanner s1, Scanner s2) {
        int overlapCount = 0;
        for (int[][] rotationMatrix : Scanner.ROTATIONS) {
            Scanner rs2 = s2.rotate(rotationMatrix);
            int overlaps = s1.computeCommonBeacons(rs2);
            if (overlaps > overlapCount) {
                overlapCount = overlaps;
                if (overlaps >= Scanner.MINIMUM_COMMON_BEACONS) {
                    s2.originPosition = rs2.originPosition;
                    s2.rotationMatrix = rotationMatrix;
                    s2.beacons = rs2.beacons;
                    break;
                }
            }
        }
    }

    private boolean done() {
        for (Scanner scanner : this.scanners.values()) {
            if (!scanner.isOriented()) {
                return false;
            }
        }
        return true;
    }

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

    void run() {
        long startTimeMillis = System.currentTimeMillis();
        initData();
        findOverlappingBeacons();
        Set<int[]> beacons = new HashSet<>();
        for (String scannerName : this.scanners.keySet()) {
            for (int[] beacon : this.scanners.get(scannerName).beacons) {
                if (null != this.scanners.get(scannerName).originPosition) {
                    if (null != this.scanners.get(scannerName).rotationMatrix) {
                        int[] translatedBeacon = this.scanners.get(scannerName).translate(beacon);
                        if (-1 == this.scanners.get(scannerName).find(translatedBeacon,
                                beacons.toArray(new int[][]{ }))) {
                            beacons.add(translatedBeacon);
                        }
                    }
                }
            }
        }
        long endTimeMillis = System.currentTimeMillis();
        System.err.println("beacon count: " + beacons.size());
        System.err.println("Elapsed time: " + elapsedTime(startTimeMillis, endTimeMillis));
        return;
    }

    private String elapsedTime(long startTimeMillis, long endTimeMillis) {
        long elapsedMillis = endTimeMillis - startTimeMillis;
        final long hr = TimeUnit.MILLISECONDS.toHours(elapsedMillis);
        final long min = TimeUnit.MILLISECONDS.toMinutes(elapsedMillis - TimeUnit.HOURS.toMillis(hr));
        final long sec =
                TimeUnit.MILLISECONDS.toSeconds(elapsedMillis - TimeUnit.HOURS.toMillis(hr) - TimeUnit.MINUTES.toMillis(min));
        final long ms =
                TimeUnit.MILLISECONDS.toMillis(elapsedMillis - TimeUnit.HOURS.toMillis(hr) - TimeUnit.MINUTES.toMillis(min) - TimeUnit.SECONDS.toMillis(sec));
        return String.format("%02dh %02dm %02d.%03ds", hr, min, sec, ms);
    }
}
