package org.cbritton.aoc.year2021.day20;

class Point implements Comparable<Point> {

    int x = 0;
    int y = 0;

    Point() {
    }

    Point(int x, int y) {
        this.x =x;
        this.y =y;
    }

    @Override
    public int compareTo(Point other) {
        return this.x != other.x ? this.x - other.x : this.y - other.y;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }

        Point point = (Point) o;

        if (x != point.x) {
            return false;
        }
        return y == point.y;
    }

    @Override
    public int hashCode() {
        int result = x;
        return 31 * result + y;
    }

    public String toString() {
        return "(" + this.x + "," + this.y + ")";
    }
}
