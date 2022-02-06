package org.cbritton.aoc.year2021.day20;

import java.util.HashSet;
import java.util.Set;

public class Image {

    private Set<Point> data = null;

    int minX = Integer.MAX_VALUE;
    int maxX = Integer.MIN_VALUE;
    int minY = Integer.MAX_VALUE;
    int maxY = Integer.MIN_VALUE;

    boolean isExtendedPixelsLit = false;

    public Image() {
        this.data = new HashSet<>();
    }

    void add(Point point) {

        this.data.add(point);
        if (point.x < this.minX) {
            this.minX = point.x;
        }
        if (point.x > this.maxX) {
            this.maxX = point.x;
        }
        if (point.y < this.minY) {
            this.minY = point.y;
        }
        if (point.y > this.maxY) {
            this.maxY = point.y;
        }
        return;
    }

    boolean isPixelLit(Point point) {
        if ((point.x < this.minX) || (point.x > this.maxX)
                || (point.y < this.minY) || (point.y > this.maxY)) {
            return this.isExtendedPixelsLit;
        }
        return this.data.contains(point);
    }

    int getLitPixelCount() {
        return data.size();
    }

    void printImage() {
        printImage(this.minX, this.maxX, this.minY, this.maxY);
        return;
    }

    void printImage(int minX, int maxX, int minY, int maxY) {

        System.out.println("isExtendedPixelsLit: " + this.isExtendedPixelsLit);
        for (int y = minY; y <= maxY; ++y) {
            for (int x = minX; x <= maxX; ++x) {
                if (data.contains(new Point(x, y))) {
                    System.out.print("#");
                } else {
                    System.out.print(".");
                }
            }
            System.out.println();
        }
        return;
    }
}
