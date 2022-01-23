package org.cbritton;

import java.util.concurrent.TimeUnit;

public class TimeUtil {

    public static String elapsedTime(long startTimeMillis, long endTimeMillis) {

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
