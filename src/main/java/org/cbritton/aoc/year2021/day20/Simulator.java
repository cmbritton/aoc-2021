package org.cbritton.aoc.year2021.day20;

import static org.cbritton.TimeUtil.elapsedTime;

class Simulator {

    private static final int PART_1_ENHANCEMENT_COUNT = 2;
    private static final int PART_2_ENHANCEMENT_COUNT = 48;

    Image image = null;
    Enhancer enhancer = null;

    private static final Simulator instance = new Simulator();

    public static Simulator getInstance() {
        return instance;
    }

    // 83298 is too high
    // 78730 is too high
    // 78542 is too high
    // 46232 is wrong

    void run(Image image, Enhancer enhancer) {

        long startTimeMillis = System.currentTimeMillis();
        this.image = image;
        this.enhancer = enhancer;

        for (int i = 0; i < PART_1_ENHANCEMENT_COUNT; ++i) {
            this.image = enhancer.enhance(this.image);
        }
//        System.out.println("\n\n");
//        this.image.printImage();
        long endTimeMillis = System.currentTimeMillis();
        System.out.println("\nPart 1:");
        System.out.println("    Lit pixel count: " + this.image.getLitPixelCount());
        System.out.println("    Elapsed time: " + elapsedTime(startTimeMillis, endTimeMillis));

        startTimeMillis = System.currentTimeMillis();
        for (int i = 0; i < PART_2_ENHANCEMENT_COUNT; ++i) {
            this.image = enhancer.enhance(this.image);
        }
        System.out.println("\n\n");
        this.image.printImage();

        endTimeMillis = System.currentTimeMillis();
        System.out.println("\nPart 2:");
        System.out.println("    Lit pixel count: " + this.image.getLitPixelCount());
        System.out.println("    Elapsed time: " + elapsedTime(startTimeMillis, endTimeMillis));

        return;
    }
}
