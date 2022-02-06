package org.cbritton.aoc.year2021.day20;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import static org.cbritton.TimeUtil.elapsedTime;

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
        App app = new App();
        app.run();
    }

    void run() throws IOException {
        Data data = initData();
        Simulator.getInstance().run(data.image, data.enhancer);
    }

    private Data initData() throws IOException {

        long startTimeMillis = System.currentTimeMillis();
        List<String> input = Files.readAllLines(Path.of("data/day20.data"));

        int[] algorithm = new int[input.get(0).length()];
        for (int i = 0; i < algorithm.length; ++i) {
            if (input.get(0).charAt(i) == '.') {
                algorithm[i] = 0;
            } else {
                algorithm[i] = 1;
            }
        }
        Data data = new Data();
        data.enhancer = new Enhancer(algorithm);

        List<String> imageDataStr = input.subList(2, input.size());
        int rows = imageDataStr.size();
        int cols = imageDataStr.get(0).length();
        data.image = new Image();
        for (int x = 0; x < rows; ++x) {
            for (int y = 0; y < cols; ++y) {
                if (imageDataStr.get(x).charAt(y) == '#') {
                    data.image.add(new Point(x, y));
                }
            }
        }
        long endTimeMillis = System.currentTimeMillis();
        System.out.println("\nInit data:");
        System.out.println("    Elapsed time: " + elapsedTime(startTimeMillis, endTimeMillis));

        return data;
    }


    private static class Data {
        private Image image = null;
        private Enhancer enhancer = null;
    }
}