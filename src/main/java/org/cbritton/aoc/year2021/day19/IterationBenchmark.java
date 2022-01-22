package org.cbritton.aoc.year2021.day19;

import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class IterationBenchmark {

    private final int OBJ_COUNT = 10000;

    void run() {

        System.err.println("Object count: " + NumberFormat.getInstance().format(OBJ_COUNT));

        testMapKeys();
        testMapValues();
        testArrayList();
        testArray();
        testArrayIndex();

        return;
    }

    private void testArrayIndex() {
        List<MyObject> list = new ArrayList<>();
        MyObject[] array = null;
        for (int i = 0; i < OBJ_COUNT; ++i) {
            MyObject myObject = new MyObject("Object " + i, i);
            list.add(myObject);
        }
        array = list.toArray(new MyObject[]{ });
        long startTimeMillis = System.currentTimeMillis();
        for (int i = 0; i < array.length; ++i) {
            MyObject myObject = array[i];
            for (int j = 0; j < array.length; ++j) {
                MyObject myObject2 = array[j];
                if (!myObject.name.equals(myObject2.name)) {
                    ++myObject.id;
                }
            }
        }
        long endTimeMillis = System.currentTimeMillis();
        System.err.println("Iterate array index elapsed time: " + elapsedTime(startTimeMillis, endTimeMillis));
        return;
    }

    private void testArray() {
        List<MyObject> list = new ArrayList<>();
        MyObject[] array = null;
        for (int i = 0; i < OBJ_COUNT; ++i) {
            MyObject myObject = new MyObject("Object " + i, i);
            list.add(myObject);
        }
        array = list.toArray(new MyObject[]{ });
        long startTimeMillis = System.currentTimeMillis();
        for (MyObject myObject : array) {
            for (MyObject myObject2 : array) {
                if (!myObject.name.equals(myObject2.name)) {
                    ++myObject.id;
                }
            }
        }
        long endTimeMillis = System.currentTimeMillis();
        System.err.println("Iterate array foreach elapsed time: " + elapsedTime(startTimeMillis, endTimeMillis));
        return;
    }

    private void testArrayList() {
        List<MyObject> list = new ArrayList<>();
        for (int i = 0; i < OBJ_COUNT; ++i) {
            MyObject myObject = new MyObject("Object " + i, i);
            list.add(myObject);
        }
        long startTimeMillis = System.currentTimeMillis();
        for (MyObject myObject : list) {
            for (MyObject myObject2 : list) {
                if (!myObject.name.equals(myObject2.name)) {
                    ++myObject.id;
                }
            }
        }
        long endTimeMillis = System.currentTimeMillis();
        System.err.println("Iterate ArrayList elapsed time: " + elapsedTime(startTimeMillis, endTimeMillis));
        return;
    }

    private void testMapValues() {
        Map<String, MyObject> map = new HashMap<>();
        for (int i = 0; i < OBJ_COUNT; ++i) {
            MyObject myObject = new MyObject("Object " + i, i);
            map.put(myObject.name, myObject);
        }
        long startTimeMillis = System.currentTimeMillis();
        for (MyObject myObject : map.values()) {
            for (MyObject myObject2 : map.values()) {
                if (!myObject.name.equals(myObject2.name)) {
                    ++myObject.id;
                }
            }
        }
        long endTimeMillis = System.currentTimeMillis();
        System.err.println("Iterate HashMap values elapsed time: " + elapsedTime(startTimeMillis, endTimeMillis));
        return;
    }

    private void testMapKeys() {
        Map<String, MyObject> map = new HashMap<>();
        for (int i = 0; i < OBJ_COUNT; ++i) {
            MyObject myObject = new MyObject("Object " + i, i);
            map.put(myObject.name, myObject);
        }
        long startTimeMillis = System.currentTimeMillis();
        for (String name : map.keySet()) {
            for (String name2 : map.keySet()) {
                MyObject myObject = map.get(name);
                MyObject myObject2 = map.get(name2);
                if (!myObject.name.equals(myObject2.name)) {
                    ++myObject.id;
                }
            }
        }
        long endTimeMillis = System.currentTimeMillis();
        System.err.println("Iterate HashMap keyset elapsed time: " + elapsedTime(startTimeMillis, endTimeMillis));
        return;
    }

    private String elapsedTime(long startTimeMillis, long endTimeMillis) {
        return String.format("%,d ms", endTimeMillis - startTimeMillis);
    }

    public static void main(String[] args) {
        IterationBenchmark iterationBenchmark = new IterationBenchmark();
        iterationBenchmark.run();
    }


    private static class MyObject {

        String name = null;
        int id = 0;

        public MyObject(String name, int id) {
            this.name = name;
            this.id = id;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;

            MyObject myObject = (MyObject) o;

            if (id != myObject.id) return false;
            return name != null ? name.equals(myObject.name) : myObject.name == null;
        }

        @Override
        public int hashCode() {
            int result = name != null ? name.hashCode() : 0;
            result = 31 * result + id;
            return result;
        }
    }
}
