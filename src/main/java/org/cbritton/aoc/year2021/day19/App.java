package org.cbritton.aoc.year2021.day19;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.cbritton.TimeUtil.elapsedTime;
import static org.cbritton.aoc.year2021.day19.Rotation.IDENTITY_MATRIX;

/**
 * Reads the simulation data and runs the simulation.
 */
public class App {

    /**
     * Runs the simulation.
     * @param args command line arguments
     * @throws IOException if an error occurs reading the simulation data from disk
     */
    public static void main(String[] args) throws IOException {
        Simulator.getInstance().run(initData());
    }

    /**
     * Reads puzzle data and creates a map of scanners.
     * @return a map of scanners
     * @throws IOException if an error occurs reading the file from disk
     */
    private static Map<String, Scanner> initData() throws IOException {

        long startTimeMillis = System.currentTimeMillis();
        Map<String, Scanner> scanners = new HashMap<>();
        List<String> data = Files.readAllLines(Path.of("data/day19.data"));

        List<int[]> beacons = new ArrayList<>();
        String scannerName = null;

        for (String line : data) {
            if (line.startsWith("---")) {
                if (!beacons.isEmpty()) {
                    scanners.put(scannerName, new Scanner(scannerName, beacons.toArray(new int[][] { })));
                }
                beacons.clear();
                scannerName = "scanner " + line.split(" ")[2];
                continue;
            }
            if (!line.isBlank()) {
                String[] values = line.strip().split(",");
                beacons.add(new int[] { Integer.parseInt(values[0]), Integer.parseInt(values[1]),
                        Integer.parseInt(values[2]) });
            }
        }

        scanners.put(scannerName, new Scanner(scannerName, beacons.toArray(new int[][] { })));
        Scanner scanner = scanners.get("scanner 0");
        scanner.originPosition = new int[] { 0, 0, 0 };
        scanner.rotationMatrix = IDENTITY_MATRIX;

        long endTimeMillis = System.currentTimeMillis();
        System.out.println("\nInit data:");
        System.out.println("    Elapsed time: " + elapsedTime(startTimeMillis, endTimeMillis));
        return scanners;
    }
}